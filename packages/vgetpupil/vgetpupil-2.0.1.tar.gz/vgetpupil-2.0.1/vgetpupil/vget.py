import argparse
import sys
import cv2
import csv
import time
from pupil_detectors import Detector2D
import json
import os

detector = Detector2D()


# This function is to display progressive bar
def print_percent_done(index_input, total, bar_len=50, title_input='Please wait'):
    percent_done = (index_input + 1) / total * 100
    percent_done_round = round(percent_done, 1)

    done = int(round(percent_done_round / (100 / bar_len)))
    togo = bar_len - done

    done_str = '█' * done
    togo_str = '░' * togo

    sys.stdout.write(f'\r{title_input}: [{done_str}{togo_str}] {percent_done_round}% done')


# This function is to change from frame count to frame time to be used as pupil time
def frame_to_time(frame_number, frame_rate):
    return frame_number / frame_rate


# This function is to get the positions in given array
def get_position(search_input, array_in):
    idx_found = False
    return_idx = None
    for idx, val in enumerate(array_in):
        if val == search_input:
            idx_found = True
            return_idx = idx
            break

    if not idx_found:
        print(f"{search_input} can not be found!")

    return return_idx


# This function is to get the direction from disk condition string
def get_direction(disk_condition_string):
    if "left" in str(disk_condition_string):
        direction = -1
    elif "right" in str(disk_condition_string):
        direction = 1
    else:
        str_array = disk_condition_string.split("-")
        if str_array and len(str_array) > 0:
            try:
                direction = int(float(str_array[-1]))
            except ValueError as e:
                direction = 1
                print("Error occurs in get_direction function:", e)
        else:
            direction = 1
        if direction >= 2:
            direction = -1
    return direction


# This function is to check whether the string can be loadable by jason.loads or not
def can_be_loaded_json(input_string):
    input_string = input_string.replace("\'", "\"")
    try:
        json_object = json.loads(input_string)
    except ValueError as e:
        return False, str(e)
    return True, json_object


# This function is to get disk condition string from the string which can be loaded with json
def get_disk_condition(string_input):
    string_input = string_input.replace("\'", "\"")
    start_index = string_input.find("disk-condition")
    end_index = string_input.find("\"}")
    return string_input[start_index:end_index]


def get_trial_condition_string(event_string_input):
    successful, event_string_loaded = can_be_loaded_json(event_string_input)
    if successful:
        trial_condition_string = event_string_loaded["trial_index"]
    else:
        trial_condition_string = get_disk_condition(event_string_input)

    return trial_condition_string


def get_direction_from_info(time_input, array_input):
    earliest_time = array_input[0]["start_timestamp"]
    latest_time = array_input[-1]["end_timestamp"]
    if time_input < earliest_time or time_input > latest_time:
        return 1
    else:
        for info in array_input:
            start_time = info["start_timestamp"]
            end_time = info["end_timestamp"]
            direction = info["trial_direction"]
            if start_time <= time_input <= end_time:
                return direction


def get_trial_info(csv_input):
    with open(csv_input, "r") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        header_array = next(csv_data)
        rows = []
        for data in csv_data:
            rows.append(data)

        record_timestamp_position = get_position("record_timestamp", header_array)
        event_string_position = get_position("event_string", header_array)

        start_timestamp = 0
        trial_direction = 1
        start_marker_found = False
        trial_condition_string = ""
        trial_info_array = []
        for row in rows:
            record_timestamp = float(row[record_timestamp_position])
            event_string = row[event_string_position]

            if not start_marker_found:
                if "start_marker" in event_string:
                    trial_condition_string = get_trial_condition_string(event_string)
                    trial_direction = get_direction(trial_condition_string)
                    start_timestamp = record_timestamp
                    start_marker_found = True
            else:
                if "end_marker" in event_string:
                    end_timestamp = record_timestamp
                    trial_info = {}
                    trial_info["trial_condition"] = trial_condition_string
                    trial_info["start_timestamp"] = start_timestamp
                    trial_info["end_timestamp"] = end_timestamp
                    trial_info["trial_direction"] = trial_direction
                    trial_info_array.append(trial_info)
                    start_marker_found = False

        csv_file.close()
        return trial_info_array


def main():
    parser = argparse.ArgumentParser(prog='vgetpupil',
                                     description='VGETPUPIL package.')
    parser.add_argument('--version', action='version', version='2.0.1'),
    parser.add_argument("-i", dest="input_filename", required=True, type=argparse.FileType('r'), default=sys.stdin,
                        help="input mp4 file", metavar="filename.mp4")
    parser.add_argument("-o", dest="output_filename", required=True, type=argparse.FileType('w'), default=sys.stdout,
                        help="output csv file", metavar="filename.csv")
    parser.add_argument("-e", dest="eye_id_input", required=False, type=int, default=None, help="eye id input",
                        metavar="0 or 1")
    parser.add_argument("-c", dest="config_input", required=False, help="config input",
                        metavar="config file to adjust pupil detectors")
    parser.add_argument("-gc", dest="gaze_csv_input", required=False, help="gaze csv input",
                        metavar="gaze csv to be referenced")
    # parser.add_argument("-tc", dest="time_csv_input", required=False, help="time csv input",
    #                     metavar="timestamp csv to be referenced")

    args = parser.parse_args()
    input_file = args.input_filename.name
    output_file = args.output_filename.name
    eye_id_input_from_user = args.eye_id_input
    config_file = args.config_input
    gaze_csv_input = args.gaze_csv_input
    # time_csv_input = args.time_csv_input
    eye_side_input = None
    convert_able = True
    trial_info_array = None

    if config_file:
        detector_properties = Detector2D.get_properties(detector)
        print("<Default Detector Properties>")
        print(detector_properties)
        try:
            with open(str(config_file)) as f:
                config_info = json.load(f)
                print("<Config Detector Properties>")
                print(config_info)
                detector_properties = config_info
            Detector2D.update_properties(detector, detector_properties)
            updated_properties = Detector2D.get_properties(detector)
            print("<Updated Detector Properties>")
            print(updated_properties)
        except Exception as error:
            print(f"Error in retrieving info from config file:{config_file}!")
            print(error)

            return

    # Define conditions to decide input mp4 is left or right eye video
    left_eye_indicated_string = "left" in str(input_file).lower() or "0" in str(input_file).lower()
    right_eye_indicated_string = "right" in str(input_file).lower() or "1" in str(input_file).lower()

    # Handle error for type of input file
    if str(input_file).endswith(".mp4"):
        if eye_id_input_from_user == 0 or eye_id_input_from_user == 1:
            eye_side_input = eye_id_input_from_user

            # Handle warning when the force eye id input is opposite with the file name
            if eye_id_input_from_user == 1 and left_eye_indicated_string:
                print("Warning! Eye id input is not compatible with input file name.")
                print(f"Eye id input is {eye_id_input_from_user}.")
                print(f"Input file name is {input_file}.")

            # Handle warning when the force eye id input is opposite with the file name
            if eye_id_input_from_user == 0 and right_eye_indicated_string:
                print("Warning! Eye id input is not compatible with input file name.")
                print(f"Eye id input is {eye_id_input_from_user}.")
                print(f"Input file name is {input_file}.")

        # Handle error of invalid input when force eye id input is not 0 and 1
        elif eye_id_input_from_user is not None and (eye_id_input_from_user > 1 or eye_id_input_from_user < 0):
            print("Invalid eye id put! It must be 0 or 1.")
            convert_able = False

        # Handle when there is no force eye id input
        elif eye_id_input_from_user is None:
            if left_eye_indicated_string:
                eye_side_input = 0
            elif right_eye_indicated_string:
                eye_side_input = 1
            else:
                print("The input file name must contains \"left\" or \"right\" or \"0\" or \"1\".")
                print("                               (or)")
                print("We can force eye id input as \"-e 0 or -e 1\"")
                convert_able = False
    else:
        convert_able = False
        print("Input file must be mp4.")

    # Handle error when the output file name is not csv
    if str(output_file).endswith(".csv"):
        pass
    else:
        convert_able = False
        print("Output file must be csv.")

    if gaze_csv_input:
        if str(gaze_csv_input).endswith(".csv"):
            try:
                os.path.isfile(gaze_csv_input)
                trial_info_array = get_trial_info(gaze_csv_input)
                # for t in trial_info_array:
                #     print(t)
            except FileNotFoundError:
                convert_able = False
                print("Invalid gaze csv input.")

        else:
            convert_able = False
            print("Invalid gaze csv input.")

    if convert_able:
        print("Input file name:", input_file)
        print("Output file name:", output_file)
        input_video = cv2.VideoCapture(input_file)
        frame_width = input_video.get(cv2.CAP_PROP_FRAME_WIDTH)
        print("Input frame width:", frame_width)
        frame_height = input_video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print("Input frame height:", frame_height)
        frame_rate = input_video.get(cv2.CAP_PROP_FPS)
        print("Input frame rate:", frame_rate)
        frame_count = input_video.get(cv2.CAP_PROP_FRAME_COUNT)
        print("Input frame count:", frame_count)

        # Open the output file to write the data
        with open(output_file, mode='w', newline="") as destination_file:
            header_names = ["pupil_time", "record_timestamp", "direction", "eye_id", "confidence", "x_nom",
                            "y_nom", "diameter", "ellipse_center_x", "ellipse_center_y",
                            "ellipse_axis_a", "ellipse_axis_b", "ellipse_angle"]
            csv_writer = csv.DictWriter(destination_file, fieldnames=header_names)
            csv_writer.writeheader()

            w_start = time.time()
            count = 0

            while True:
                # r_start = time.time()
                ret, frame = input_video.read()
                print_percent_done(count, frame_count)
                # r_stop = time.time()
                # print(f"read time {(r_stop - r_start) * 1000}")

                # When there is frame to read
                if ret:
                    pupil_time = frame_to_time(count, frame_rate)
                    count += 1
                    cur_time = time.time()
                    # print(pupil_time)
                    # print(type(frame))
                    eye_id = eye_side_input
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    # d_start = time.time()
                    result = detector.detect(gray)
                    # d_stop = time.time()
                    # print(f"detecter time {(d_stop - d_start) * 1000} milisec")
                    confidence = result["confidence"]
                    ellipse = result["ellipse"]
                    ellipse_center_x = ellipse["center"][0]
                    ellipse_center_y = ellipse["center"][1]
                    ellipse_axis_a = ellipse["axes"][0]
                    ellipse_axis_b = ellipse["axes"][0]
                    ellipse_angle = ellipse["angle"]
                    diameter = result["diameter"]
                    x_nom = ellipse_center_x / 192
                    y_nom = ellipse_center_y / 192
                    if gaze_csv_input and trial_info_array:
                        direction_input = get_direction_from_info(pupil_time, trial_info_array)
                    else:
                        direction_input = "None"
                    data_to_write = {"pupil_time": pupil_time,
                                     "record_timestamp": pupil_time,
                                     "direction": direction_input,
                                     "eye_id": eye_id,
                                     "confidence": confidence,
                                     "x_nom": x_nom,
                                     "y_nom": y_nom,
                                     "diameter": diameter,
                                     "ellipse_center_x": ellipse_center_x,
                                     "ellipse_center_y": ellipse_center_y,
                                     "ellipse_axis_a": ellipse_axis_a,
                                     "ellipse_axis_b": ellipse_axis_b,
                                     "ellipse_angle": ellipse_angle, }
                    csv_writer.writerow(data_to_write)
                    # print(f"process time {(time.time() - cur_time) * 1000}")
                    # print(f"one loop time {(time.time() - r_start) * 1000}")

                # When there is no frame to read
                else:
                    input_video.release()
                    cv2.destroyAllWindows()
                    destination_file.close()
                    break

        # w_stop = time.time()
        # print(f"whole time {(w_stop - w_start) / 60}")
