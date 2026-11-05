import discord, time, requests, math, os
from discord.ext import tasks

serverId = 1558579019669315694
defaultRoleId = 1567195682048057475
adminIds = [754431586815967284, 184768535107469314]

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

welcomeChannelId = 1567199477306237009
botChannelId = 1567205782607368252
memberLastMessage = {}
memberXPdict = {}

sheetsToken = os.getenv("SHEETS_API")

pronounsMessageId = 1567291884853010553
disableStreamPingsId = 1567291895917576324

levelColourList = [0xA0D0FF, 0xA0C0FF, 0xA0B0FF, 0xA0A0FF, 0xC0A0FF, 0xE0A0FF, 0xFFA0FF, 0xFFA0E0, 0xFFA0C0, 0xFFA0A0, 0xFFB0A0, 0xFFC0A0, 0xFFE0A0, 0xFFFFA0]

joinColour = 0x40FF60
leaveColour = 0xFF4060

# tests whatever im working on
@tree.command(name="test",
              description=f"tests whatever im working on",
              guild=discord.Object(id=serverId))
async def test(interaction: discord.Interaction):
    if interaction.user.id not in adminIds:
        await interaction.response.send_message("only for bot admins (for testing)", ephemeral=True)
        return

    await interaction.response.send_message(memberXPdict, ephemeral=True)

# talk through the bot
@tree.command(name="talk",
              description=f"talk as the bot",
              guild=discord.Object(id=serverId))
async def talk(interaction: discord.Interaction, text_to_send: str):
    if interaction.user.id not in adminIds:
        await interaction.response.send_message("only for bot admins", ephemeral=True)
        return 

    await interaction.response.defer(ephemeral=True)
    await interaction.channel.send(text_to_send)
    await interaction.delete_original_response()

# check bot ping
@tree.command(name="level",
              description=f"check your level progress",
              guild=discord.Object(id=serverId))
async def ping(interaction: discord.Interaction):
    userId = interaction.user.id

    try:
        xp, level = memberXPdict[userId]
    except KeyError:
        await interaction.response.send_message(f"you dont have a level yet", ephemeral=True)
        return

    XPneededToLevelUp = (level + 1) * 3

    await interaction.response.send_message(f"Level: {level}\nXP: {xp}/{XPneededToLevelUp} ({format(xp/XPneededToLevelUp*100, ".2f")}%)")

# check bot ping
@tree.command(name="ping",
              description=f"check the bots ping",
              guild=discord.Object(id=serverId))
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"pong 🏓 {client.latency * 1000:.2f}ms", ephemeral=True)

# adds role to member
async def addReactionRole(member, roleId):
    role = discord.utils.get(member.guild.roles, id=roleId)
    await member.add_roles(role)
    await member.send(f"`{role}` added as a role")

# when any message gets reacted to
@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if payload.message_id != pronounsMessageId and payload.message_id != disableStreamPingsId:
        return

    emoji = payload.emoji.name

    match emoji:
        case "🧫": await addReactionRole(payload.member, 1567287979880349778)
        case "📡": await addReactionRole(payload.member, 1567288010264027188)
        case "🎑": await addReactionRole(payload.member, 1567288043780448357)
        case "🛼": await addReactionRole(payload.member, 1567288057588228196)
        case "🏪": await addReactionRole(payload.member, 1567288072683655290)
        case "🇧🇷": await addReactionRole(payload.member, 1567288085958631464)
        case "🧆": await addReactionRole(payload.member, 1567288103146754118)
        case "🎣": await addReactionRole(payload.member, 1567288122260197467)
        case "🔕": await addReactionRole(payload.member, 1567289812178829482)


# removes role from member
async def removeReactionRole(member, roleId):
    role = discord.utils.get(member.guild.roles, id=roleId)
    await member.remove_roles(role)
    await member.send(f"`{role}` removed as a role")


# when any message gets reacted to
@client.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    if payload.message_id != pronounsMessageId and payload.message_id != disableStreamPingsId:
        return

    # i have to do this only for role remove its so stupid
    emoji = payload.emoji.name
    guild = client.get_guild(payload.guild_id)
    member = discord.utils.get(guild.members, id=payload.user_id)

    match emoji:
        case "🧫": await removeReactionRole(member, 1567287979880349778)
        case "📡": await removeReactionRole(member, 1567288010264027188)
        case "🎑": await removeReactionRole(member, 1567288043780448357)
        case "🛼": await removeReactionRole(member, 1567288057588228196)
        case "🏪": await removeReactionRole(member, 1567288072683655290)
        case "🇧🇷": await removeReactionRole(member, 1567288085958631464)
        case "🧆": await removeReactionRole(member, 1567288103146754118)
        case "🎣": await removeReactionRole(member, 1567288122260197467)
        case "🔕": await removeReactionRole(member, 1567289812178829482)


# member join
@client.event
async def on_member_join(member):
    defaultRole = discord.utils.get(member.guild.roles, id=defaultRoleId)
    await member.add_roles(defaultRole)

    channel = client.get_channel(welcomeChannelId)

    messageEmbed = discord.Embed(colour=joinColour)
    messageEmbed.title = f"🛬 **{member.name}** landed in losecord↑"
    messageEmbed.description = f"-# <@{member.id}> <t:{int(time.time())}:f>"

    welcomeMessage = await channel.send(embed=messageEmbed)
    await welcomeMessage.add_reaction("🛬")

    # when person joins, check if they reacted to anything in reaction roles

# member leaves
@client.event
async def on_member_remove(member):
    channel = client.get_channel(welcomeChannelId)

    messageEmbed = discord.Embed(colour=leaveColour)
    messageEmbed.title = f"🛫 **{member.name}** departed from losecord↑"
    messageEmbed.description = f"-# <@{member.id}> <t:{int(time.time())}:f>"

    welcomeMessage = await channel.send(embed=messageEmbed)
    await welcomeMessage.add_reaction("🛫")

async def addRole(author, roleId):
    role = discord.utils.get(author.guild.roles, id=roleId)
    await author.add_roles(role)

# on message sent
@client.event
async def on_message(message):
    author = message.author
    userID = author.id

    if userID not in memberLastMessage.keys() or time.time() > memberLastMessage[userID] + 30:
        memberLastMessage[userID] = time.time()  
      
        try:
            memberCurrentXP = memberXPdict[userID][0]
            memberCurrentLevel = memberXPdict[userID][1]

            memberCurrentXP += 1
            if memberCurrentXP >= (memberCurrentLevel + 1) * 3: # >= incase i ever edit the value
                memberCurrentLevel += 1 
                memberCurrentXP = 0

                if memberCurrentLevel % 5 == 0:
                    match memberCurrentLevel:
                        case 5: await addRole(author, 1567420684819365908)
                        case 10: await addRole(author, 1567421165155393626)
                        case 15: await addRole(author, 1567421306306166864)
                        case 20: await addRole(author, 1567421357992714310)  
                        case 25: await addRole(author, 1567421437449609247)
                        case 30: await addRole(author, 1567421552579055657)
                        case 35: await addRole(author, 1567433015167295538)
                        case 40: await addRole(author, 1567433086008823898)
                        case 45: await addRole(author, 1567433182456840222)
                        case 50: await addRole(author, 1567433263830536212)
                        case 55: await addRole(author, 1567433322827874434)
                        case 60: await addRole(author, 1567438282852147282)
                        case 65: await addRole(author, 1567438294722150460)

                botChannel = client.get_channel(botChannelId)

                levelColourIndex = math.floor(memberCurrentLevel / 5)
                try:
                    levelColour = levelColourList[levelColourIndex]
                except IndexError:
                    levelColour = levelColourList[-1]

                messageEmbed = discord.Embed(colour=levelColour)
                messageEmbed.description = f"<@{userID}> leveled ↑ to **level {memberCurrentLevel}**!"

                await botChannel.send(embed=messageEmbed)

            memberXPdict[userID] = [memberCurrentXP, memberCurrentLevel]

        except KeyError: # first XP gain from user
            memberXPdict[userID] = [1, 0] # 1 xp, level 0

    if message.content == "<a:giggleler:1567287125546770493>":
        await message.add_reaction("<a:giggleler:1567287125546770493>")

# saves the XP dict to spreadsheet every 
@tasks.loop(seconds=300)
async def updateSheet():
    xp_data_array = list(zip(*[[f"'{name}", level_data[0], level_data[1]] for name, level_data in memberXPdict.items()]))
    xp_data_json = {
    "userID": xp_data_array[0],
    "userXP": xp_data_array[1],
    "userLevel": xp_data_array[2],
    }

    requests.post(sheetsToken, json=xp_data_json)

# on bot started
@client.event
async def on_ready():
    try:
        synced = await tree.sync(guild=discord.Object(id=serverId))
        print(f"<@{client.user.id}> went online <t:{int(time.time())}:R>. {len(synced)} tree commands synced.")

    except Exception as e:
        print(e)

    response_data = requests.get(sheetsToken)
    tempXPdict = dict(response_data.json())

    for i in range(len(tempXPdict["userID"])):
        userID = tempXPdict["userID"][i]
        userXP = tempXPdict["userXP"][i]
        userLevel = tempXPdict["userLevel"][i]

        memberXPdict[int(userID)] = [userXP, userLevel]

    updateSheet.start()

client.run(os.getenv("TOKEN"))