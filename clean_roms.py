import os, sys, argparse
import operator

class ALL_ROMS():
    def __init__(self, root_dir, delete):
        self.root_dir = root_dir
        self.delete = delete
        self.roms = {}

    def get_roms(self):
        rom_list = 'roms.txt'
        if os.path.exists(rom_list):
            print('using cached list from: {}'.format(rom_list))
            with open(rom_list, 'r') as fd:
                game_list = [line.strip() for line in fd.readlines()]
        else:
            game_list = []
            for dirname, dirnames, filenames in os.walk(self.root_dir):
                # print path to all filenames.
                for filename in filenames:
                    aFile = os.path.join(dirname, filename)
                    game_list.append(aFile)
            with open(rom_list, 'w') as fd:
                for f in game_list:
                    fd.write('{}\n'.format(f))
        return game_list

    def add_rom(self, rom_obj):
        if rom_obj.stripped_filename not in self.roms:
            self.roms[rom_obj.stripped_filename] = {}
            self.roms[rom_obj.stripped_filename]['roms'] = []
        self.roms[rom_obj.stripped_filename]['roms'].append(rom_obj)

    def clean(self):
        total_files = 0
        for stripped_filename, roms in self.roms.items():
            if len(roms['roms']) > 1:
                print(stripped_filename)
                have_marked = False
                delete_txt = 'OK'
                for r in sorted(roms['roms'], key=lambda x: x.weight, reverse=True):
                    total_files += 1
                    print('\t:{}:{}:{}'.format(delete_txt, r.weight, r.base_filename))
                    if have_marked is True and self.delete is True:
                        print('\tDeleting: {}'.format(r.full_path_filename))
                        os.remove(r.full_path_filename)
                    if have_marked is False:
                        have_marked = True
                        delete_txt = 'KO'

        print('total unique files: {}'.format(len(self.roms)))
        print('total files       : {}'.format(total_files))


class Rom():
    def __init__(self, full_path_filename):
        # super mario (hack) (!).nes:
        self.full_path_filename = full_path_filename
        self.base_filename, \
        self.stripped_filename, \
        self.tokens, \
        self.base_filename = self.describe_rom(full_path_filename)
        self.weight = self.calculate_weight()

    # Helper function:
    def find(self, s, ch):
        return [i for i, ltr in enumerate(s) if ltr == ch]

    # Extraction tags:
    def describe_rom(self, full_path_filename):
        # Return variables:
        ret_base_filename = ''
        ret_stripped_filename = ''
        ret_tokens = []
        ret_base_filename = os.path.basename(full_path_filename)

        # Get all the tokens:
        s_p = self.find(ret_base_filename, '(')
        e_p = self.find(ret_base_filename, ')')
        s_b = self.find(ret_base_filename, '[')
        e_b = self.find(ret_base_filename, ']')
        for i in range(len(s_p)):
            ret_tokens.append(ret_base_filename[s_p[i]:e_p[i] + 1])
        for i in range(len(s_b)):
            ret_tokens.append(ret_base_filename[s_b[i]:e_b[i] + 1])
        ret_stripped_filename = ret_base_filename
        for m in ret_tokens:
            ret_stripped_filename = ret_stripped_filename.replace(m, '')
        ret_stripped_filename = ret_stripped_filename[:-4].strip() + ret_base_filename[-4:]

        return ret_base_filename, ret_stripped_filename, ret_tokens, ret_base_filename

    # Calculate a weight for easy sorting:
    def calculate_weight(self):
        # http://www.theisozone.com/tutorials/other/general/know-your-roms-a-guide-to-identifying-the-symbols/
        priorities = [
        {'token': '[a]',   'weight': 9,   'description': 'Alternate'},
        {'token': '[b]',   'weight': -99, 'description': 'Bad Dump'},
        {'token': '[BF]',  'weight': 7,   'description': 'Bung Fix'},
        {'token': '[c]',   'weight': 8,   'description': 'Cracked'},
        {'token': '[f]',   'weight': 6,   'description': 'Other Fix'},
        {'token': '[h]',   'weight': 5,   'description': 'Hack'},
        {'token': '[o]',   'weight': 10,  'description': 'Overdump'},
        {'token': '[p]',   'weight': 4,   'description': 'Pirate'},
        {'token': '(Pirate)',   'weight': 4,   'description': 'Pirate'},
        {'token': '[t]',   'weight': 3,   'description': 'Trained'},
        {'token': '[T]',   'weight': 2,   'description': 'Translation'},
        {'token': '(Unl)', 'weight': 1,   'description': 'Unlicensed'},
        {'token': '[x]',   'weight': -99, 'description': 'Bad Checksum'},
        {'token': '[!]',   'weight': 100, 'description': 'Verified Good Dump'},
        {'token': '(a)',   'weight': 80,  'description': 'Australian'},
        {'token': '(Asia)',   'weight': 0,  'description': 'Asia'},
        {'token': '(Beta)',   'weight': -70,  'description': 'Beta'},
        {'token': '(Beta 1)',   'weight': -70,  'description': 'Beta'},
        {'token': '(Beta 2)',   'weight': -70,  'description': 'Beta'},
        {'token': '(C)',   'weight': 0,   'description': 'Chinese'},
        {'token': '(Demo)',   'weight': -20,   'description': 'Demo'},
        {'token': '(E)',   'weight': 85,  'description': 'Europe'},
        {'token': '(Europe)',   'weight': 85,  'description': 'Europe'},
        {'token': '(En)',   'weight': 95,  'description': 'English'},
        {'token': '(F)',   'weight': 0,   'description': 'French'},
        {'token': '(FN)',  'weight': 0,   'description': 'Finland'},
        {'token': '(G)',   'weight': 0,   'description': 'German'},
        {'token': '(GR)',  'weight': 0,   'description': 'Greece'},
        {'token': '(HK)',  'weight': 0,   'description': 'Hong Kong'},
        {'token': '(I)',   'weight': 0,   'description': 'Italian'},
        {'token': '(J)',   'weight': 0,   'description': 'Japan'},
        {'token': '(Ja)',   'weight': 0,   'description': 'Japan'},
        {'token': '(Japan)',   'weight': 0,   'description': 'Japan'},
        {'token': '(K)',   'weight': 0,   'description': 'Korean'},
        {'token': '(NL)',  'weight': 0,   'description': 'Dutch'},
        {'token': '(PD)',  'weight': 80,  'description': 'Public Domain'},
        {'token': '(Proto)',  'weight': -50,  'description': 'Prototype'},
        {'token': '(Proto 1)',  'weight': -50,  'description': 'Prototype'},
        {'token': '(Proto 2)',  'weight': -50,  'description': 'Prototype'},
        {'token': '(Proto 3)',  'weight': -50,  'description': 'Prototype'},
        {'token': '(Possible Proto)',  'weight': -50,  'description': 'Prototype'},
        {'token': '(Rev 1)',   'weight': 50,   'description': 'Revision 1'},
        {'token': '(Rev 2)',   'weight': 55,   'description': 'Revision 2'},
        {'token': '(Rev 3)',   'weight': 60,   'description': 'Revision 3'},
        {'token': '(S)',   'weight': 0,   'description': 'Spanish'},
        {'token': '(SW)',  'weight': 0,   'description': 'Sweden'},
        {'token': '(U)',   'weight': 95,  'description': 'USA'},
        {'token': '(USA)',   'weight': 95,  'description': 'USA'},
        {'token': '(USA, Europe)',   'weight': 95,  'description': 'USA & Europe'},
        {'token': '(UK)',  'weight': 90,  'description': 'England'},
        {'token': '(Unk)', 'weight': 0,   'description': 'Unknown Country'},
        {'token': '(World)', 'weight': 65,   'description': 'World'},
        {'token': '(-)',   'weight': 0,   'description': 'Unknown Country'},
        {'token': '(Sachen-USA)', 'weight':10, 'description': 'found it'},
        {'token': '(Sachen-English)', 'weight':10, 'description': 'found it'},
        {'token': '(1991-05-20)', 'weight':-100, 'description': 'Fix for tmnt 2 gb'}]

        high_token_penalty = -2 * len(self.tokens)
        token_value = 0

        for token in self.tokens:
            for priority in priorities:
                if token.lower() == priority['token'].lower():
                    token_value += priority['weight']
        return token_value + high_token_penalty

# Parse command line args:
def parseArgs():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--rom_dir', help='Location where your roms are stored', default='y://')
    parser.add_argument('--delete', help='WARNING: setting this will delete the roms!', action='store_true')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    # parse args:
    args = parseArgs()
    # create the ALL_ROMS class:
    all_roms = ALL_ROMS(args.rom_dir, args.delete)
    # get the list of games:
    game_list = all_roms.get_roms()
    # create a rom object for each file:
    for full_path_filename in game_list:
        all_roms.add_rom(Rom(full_path_filename))
    all_roms.clean()
    print('all done!')
