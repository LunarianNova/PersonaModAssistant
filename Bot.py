import os, shutil, discord, time
from discord.ext import commands

client = commands.Bot(command_prefix="p5!")
client.remove_command("help")


@client.command()
async def help(ctx):
    embed = discord.Embed(title="Help Command")
    embed.add_field(name="p5!ma (Old Character ID) (New Character ID)", value="EX: p5!ma 0001 0008 will take Futaba's models and target them to Joker's and Joker's animations, meaning if you slap it into a mod then futaba will replace Joker.")
    await ctx.send(embed=embed)


@client.event
async def on_ready():
    print("Started!")


@client.command()
async def ma(ctx, old, new):
    await ctx.send("Processing...")
    clock = time.time()
    done = False
    path = 'C:\\Users\\Bloop\\Downloads\\Persona-Modding\\data.cpk_unpacked'
    for y in os.scandir(path + "\\model\\character\\" + new):
        if done == False:
            if y.name.endswith("GMD"):
                for z in os.scandir(path + "\\model\\character\\" + old):
                    if z.name.endswith("GMD"):
                        if z.name.split("_")[-2] == y.name.split("_")[-2]:
                            done = True
                            default = y.name
    print(default)
    os.system(f'C:\\Users\\Bloop\\Downloads\\Persona-Modding\\P5CharacterSwapper\\P5CharacterSwapper.exe -o "C:\\Users\\Bloop\\Downloads\\Persona-Modding\\data.cpk_unpacked\\model\\character\\{old}" -n "C:\\Users\\Bloop\\Downloads\\Persona-Modding\\data.cpk_unpacked\\model\\character\\{new}" -id "{default.split("_")[-2]}" -gap-rt')
    src = f'{path}\\model\\character\\{new}\\{default}'
    resultpath = f"{path}\\model\\character\\{new} Retargeted to {old}"
    for dname, dirs, files in os.walk(f"{path}\\model\\character\\{old}"):
        for fname in files:
            if fname.endswith(".GMD"):
                newname = fname.replace(f"c{old}", f"c{new}")
                newpath = os.path.join(f"{path}\\model\\character\\{new}\\", newname)
                if os.path.isfile(newpath):
                    shutil.copyfile(newpath, f"{resultpath}\\{fname}")
                else:
                    shutil.copyfile(src, f"{resultpath}\\{fname}")
    shutil.make_archive(resultpath, 'zip', resultpath)
    await ctx.send(f"Finished in {round(time.time()-clock)} seconds, uploading to the web, usually takes about 1-2 minutes, I will ping you when I am done")
    os.system(f'pyupload "{resultpath}.zip" --host=catbox > output.txt')
    with open('output.txt') as f:
        file = f.read()
    await ctx.send(f"File Uploaded! {file.split(': ')[-1]}<@!{ctx.author.id}>\nFiles are automatically deleted after 24 hours to save space")
    shutil.rmtree(resultpath)
    os.remove(f"{resultpath}.zip")

client.run("token")
