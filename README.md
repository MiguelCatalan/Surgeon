# Surgeon

## What is this?
**For the Android developers that love to split the strings files, will have to suffer when they have to add translations.** It is hard to know if there is a new string searching in each file for each translation and mobile network.

Surgeon it is a simple script that **finds all the string files, merges them and compares each translation to find the differences**. Finally generates a new file with the missing translations in each language.

## How do I use it?
 
- Edit the *config.py* file and put the name and the path of your project and/or other extra configurations.
- And run the script with:

		python surgeon.py
		
Easy isn't it?

## Customizable
- Define where is your project with *PROJECT_PATH*
- Search in an expecific module defining *MODULE_NAME* constant
- For a particular flavour
- You cand define if your string files has a particular prefix or suffix
- And last but no least, the result file
- What more? DIY and PR :)
	
## Don't be shy
Pull requests are more than welcome. I am not an expert in Python so lets put this newbie surgeon to the top of the wall of fame.

## License
	Copyright 2015 Miguel Catalan Bañuls

	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

		http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.

