# rom_cleaner
Trim Game Roms based on File Name

I take no responsibility for the usage of this script!

When you run it with the --delete flag, it WILL delete ROMs!

Make a backup of your ROMs before using the --delete flag!

This is a simple script that will delete your ROMs,
based on their file name.

It is guaranteed to keep 1 (and only 1) ROM of each "type".

For instance (this is safe to run... you need to explicity put the **--delete** flag actually delete stuff.)

```bash
python clean_roms.py --rom_dir /Volumes/roms
...
Challenger.nes
	:OK:-2:Challenger (J).nes
	:KO:-4:Challenger (J) [p1].nes
Wesley Tokyo Eden 05.smc
	:OK:78:Wesley Tokyo Eden 05 (PD).smc
	:KO:76:Wesley Tokyo Eden 05 (PD) [h1C].smc
Little Magic.smc
	:OK:-2:Little Magic (Beta).smc
	:KO:-4:Little Magic (Beta) [h2C].smc
	:KO:-4:Little Magic (Beta) [o1].smc
	:KO:-4:Little Magic (J) [T+Eng1.00b_AGTP].smc
	:KO:-6:Little Magic (J) [T+Eng1.00b_AGTP][a1].smc
```
It's based on a weighted system.
It's geared towards English, but feel free to modify it:

```python
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
```

When you are happy with list of "KO" (aka, the files that the script will delete), run it like so:

```bash
python clean_roms.py --rom_dir /Volumes/roms --delete
```
