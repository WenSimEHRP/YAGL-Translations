# Decompiling and encoding

This repo comes with a binary of yagl. To run yagl, you would need to either install wsl (on windows) or run it on linux.

<!--the reason I didn't include an exe is because I can't compile it grrrrrrrr-->.

# Decompiling

To decompile a NewGRF, you must first make one available.
Run it with this command;
```bash
./yagl -d your_file_name.grf
```
The program should create several png files in `sprites/` and a single `your_file_name.yagl` in the same folder.

After decompiling, you can modify the file as you like, e.g. change all default strings to `woshi liangzhichao ta nainai` or 
```
あらっつぁっつぁーやりびだびりんらばりっだんりんらんれんらんどーわばりっかったーぱりっぱりーばりびりびりびりすてんれんらんどんやばりんらんてんらんでーあろーわらばどぅぶどぅぶどぅぶどぅぶでーいぇぶーわでぃっだーりんらんれんらんどーだがたかたかとぅーとぅーでーやどぅー
```
**something related to Ievan Polkka, let's just skip that part*.

# Encoding

The steps for encoding are similar. No need to change your working directory, just stay in the same directory and type this in your console:
```bash
./yagl -e your_file_name.yagl
```
The program should create a file named `your_file_name.yagl`, but this time not in `sprites/`, rename it to whatever you like and change the extension to `.grf`. Now you can copy the file into your OpenTTD newgrf folder and try it out!