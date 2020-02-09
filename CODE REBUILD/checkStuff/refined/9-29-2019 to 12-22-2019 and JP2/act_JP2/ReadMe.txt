I've outlined below what I see as to be likely the easiest way to attach my testUpload file to your test OMR program. 
Should be simple feel free to email me or text with any questions.

	As of this moment the program simply reads every text file from the Tests folder. Checks if the test has been uploaded.
	If it has been it ignores the file, otherwise it parses and uploads the student's data.

	If you want to continue using the file in this fashion: simply update the os.chdir("./Tests") line to point to whatever directory you save to.
	WARNING: Do not have any other test files in this folder it will cause crashes.

	However to attach this to your program you will need to copy over the whole code into your program.
	I've provided capitalized markers of where each block needs to go.
	You will need to change the for loop to a single call to upload(file),
	as well as set file to the filename of your written test file.

	LASTLY:
	Before you begin uploading though I will need you to send me your public ip address so I can set it as an approved connection point.

Happy Debugging

