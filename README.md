# UnrealModAutoDeploy
This is a simple program for unreal engine 4/5 modders that is meant to speed up the process of jumping between the engine and in game.
This mod automatically detects when there is a new build of your packaged unreal engine mod in your selected directory, renames it accordingly, and moves it to your mods folder.

This is my first python program. I know the code is bad and the UI is ugly. Cut me some slack.

to use:
1. make sure your unreal project is packaging your mod as a pakchunk with "50" in the number. it could be pakchunk 50, 500, 5000, 5050, ect.
2. open ModAutoDeploy
3. Set your packaging directory to wherever you are packaging your project.
4. Set your target mods folder to your game's mods folder of choice.
5. replace Test_P in the textbox with whatever you want your mod's name to be. make sure to hit "Apply Modname" to set your modname.
6. Package your project and your mod will be automatically added to your game's mods folder
