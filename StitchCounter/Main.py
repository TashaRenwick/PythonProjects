import keyboard
import json

#TODO: Increase flexibility for patterns: What can I type in? What sort of files can I load?
#TODO: Why the double printintg lol
#TODO: Why is the row_index not saving correctly

class Tracker:
    def __init__(self):
        print("Creating instance of 'Tracker'")

        ingest_method = input('How would you like to input the pattern? Enter "file" if you have a json or "manual" otherwise: ')
        if ingest_method == "file":
            self.filepath = input('Please enter the filepath including filename for your stored pattern: ')
            self.pattern, self.row_index, self.stitch_index = self.__read_pattern(self.filepath)

        else:
            # Need to ingest the pattern, storing total number of rows
            self.total_rows = int(input("Please enter total number of rows: "))

            # Creating variables for pattern info
            self.pattern = [['', '']] * self.total_rows
            self.row_index = 0
            self.stitch_index = 0

            # Function to convert person friendly-string to computer friendly list
            def convert_string_to_pattern(string) -> list:
                '''
                Takes a string and returns a computer friendly list to iterate over. Definitely room for improvement
                :param string:
                :return list:
                '''

                # Split string by space and remove commas so we just have a list like ['5', 'aug', 'sc']
                split = string.split(' ')
                split = [x.replace(',', '') for x in split if x != '']

                # Create a list of tuples, grouping each collection of similar stitches together ie [('5', 'norm', 'sc')]
                tupled = []
                for i in range(len(split))[::3]:
                    tupled.append(tuple(split[i:i + 3]))

                # Function that takes a tuple and returns a computer-friendly list
                def list_from_tuple(t):
                    ls = [t[1] + ' ' + t[2]] * int(t[0])
                    return ls

                result = []
                for t in tupled:
                    result += list_from_tuple(t)

                return result

            # Looping through each row, setting each entry of the array to a list containing all the stitch info for that row
            for index, row in enumerate(self.pattern):
                # Input stitch pattern for row
                stitches = input(f"Please enter the stitches for row {int(index + 1)}: ")

                # Store stitch pattern for row as both human and machine-friendly
                self.pattern[index][0], self.pattern[index][1] = stitches, convert_string_to_pattern(stitches)

        print(self.pattern)
    def print_pattern(self):
        for index, row in enumerate(self.pattern):
            print(f'Row {index+1}:', row[0])

    def __read_pattern(self, filepath: str):
        f = open(filepath, 'r')
        pattern = json.load(f)
        f.close()

        return pattern['pattern'], pattern['row_index'], pattern['stitch_index']

    def __run_counter(self, row_index: int, total_stitches: int, stitch_pattern: list) -> None:
        '''

        :param row_index:
        :param total_stitches:
        :param stitch_pattern:
        :return:
        '''

        # Creating function to save pattern and exit
        def save_pattern():

            filepath = input('Please enter you filepath and filename: ')

            # Create json dict
            json2 = {
                'pattern': self.pattern,
                'row_index': self.row_index,
                'stitch_index': self.stitch_index
            }
            # Create file to save to
            f = open(filepath, 'w')

            # Write json to file
            f.write(json.dumps(json2, indent=4))

            # Close file
            f.close()
            print(f'Pattern progress saved to file: {filepath}')
            return None


        print(f'Starting row {row_index + 1}')
        print(f'Starting with stitch {self.stitch_index + 1}')

        continue_running = True
        while continue_running:
            print(f'\n Number of completed stitches: {self.stitch_index}/{total_stitches}')
            print(f'Stitch one {stitch_pattern[self.stitch_index]}')
            print("\n Press the Esc key if you'd like to save and exit: ")
            print("Press the Space key when you complete a stitch: ")

            # Wait for the next event.
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN and event.name == 'space':

                # Increment number of completed stitches
                self.stitch_index += 1

                # Check if row is complete
                if self.stitch_index == total_stitches:
                    continue_running = False

            elif event.event_type == keyboard.KEY_DOWN and event.name == 'esc':
                # Exit loop after this
                continue_running = False

                # Saving file
                save_pattern()

                print('Thank you, please come again soon!')
                exit()


        if self.stitch_index == total_stitches:
            print(f'\n {total_stitches}/{total_stitches} stitches: Row {row_index + 1} completed')

        self.stitch_index = 0
        self.row_index = 0
        return None


    def run_tracker(self):
        print('\n Starting tracker... ')

        for index, row in enumerate(self.pattern[self.row_index:]):
            # print('ROW(1): ', row[1])
            # print('STITCH_INDEX :', self.stitch_index)
            value = len(row[1])
            self.__run_counter(row_index=index, total_stitches=value, stitch_pattern=row[1])

        print('\n Pattern completed - nice one!')
        return None


tracker = Tracker()

tracker.print_pattern()
tracker.run_tracker()


