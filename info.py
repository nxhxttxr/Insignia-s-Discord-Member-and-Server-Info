import discord
from discord import app_commands
from discord.ext import commands
from time import time

class Trace(commands.GroupCog, name='info'):
    def __init__(self, client: commands.Bot):
        super().__init__()
        self.client = client

    #----------------------------------------------------TRACE----------------------------------------------------#
    @app_commands.command(name='trace', description='Displays various information on all the servers the member shares with the bot.')
    @app_commands.guild_only()
    @app_commands.describe(user = 'The user you want to display information for')
    async def info_group_trace(self, interaction: discord.Interaction, user: discord.Member):
        start_time = time()

        found_in_counter = 0
        is_owner_counter = 0
        has_toprole_counter = 0
        is_admin_counter = 0
        has_manageserver_counter = 0

        guild_names = []
        nicknames = []
        highest_roles = []
        has_admin = []
        has_manage_server = []
        is_server_owner = []
        has_top_role = []
        for guild in self.client.guilds:
            target = guild.get_member(user.id)
            if target: 
                found_in_counter += 1
                guild_names.append(guild.name)
                nicknames.append(target.display_name)

                highest = discord.utils.find(lambda role: role in target.roles, reversed(target.roles))
                if highest: highest_roles.append(highest.name)  
                else:
                    highest = 'No role found in this server'
                    highest_roles.append(highest)
                
                if guild.owner != target: is_server_owner.append('NO')
                else:
                    is_server_owner.append('YES')
                    is_owner_counter += 1

                if guild.roles[len(guild.roles)-1] != target.top_role: has_top_role.append('NO')
                else:
                    has_top_role.append('YES')
                    has_toprole_counter += 1
                
                if not target.guild_permissions.administrator: has_admin.append('NO')
                else:
                    has_admin.append('YES')
                    is_admin_counter += 1
                
                if not target.guild_permissions.manage_guild: 
                    if not target.guild_permissions.administrator: has_manage_server.append('NO')
                    else:
                        has_manage_server.append('YES')
                        has_manageserver_counter += 1
                else:
                    has_manage_server.append('YES')
                    has_manageserver_counter += 1

        if len(guild_names) == len(nicknames) and len(guild_names) == len(highest_roles) and len(guild_names) == len(has_admin) and len(guild_names) == len(has_manage_server) and len(guild_names) == len(is_server_owner) and len(guild_names) == len(has_top_role):
            end_time = time()
            print(end_time-start_time)
            desc = f"**TRACE RESULTS - CALCULATED IN {end_time-start_time}'' AT {round(self.client.latency * 1000)}ms LATENCY**\n\n"
            for i in range(len(guild_names)):
                desc = desc + f'Server Name: ``{guild_names[i]}``\n\
                    Server Nickname: ``{nicknames[i]}``\n\
                    Is Server Owner: ``{is_server_owner[i]}``\n\
                    Has Adminstrator Permission: ``{has_admin[i]}``\n\
                    Has Manage Server Permission: ``{has_manage_server[i]}``\n\
                    Has Top Role: ``{has_top_role[i]}``\n\
                    Highest Role Name: ``{highest_roles[i]}``\n\n'
            
            traceEmbed = discord.Embed(
                title=f'TRACING: {user.name}',
                description=desc,
                color=discord.Color.dark_gold()
            ).set_thumbnail(url=user.avatar).set_footer(text='Trace v2 | PROJECT UTOPIA™ by Insignia')
            traceEmbed.add_field(name='Number of servers user has been found in:', value=f'{found_in_counter}', inline=False)
            traceEmbed.add_field(name='Number of servers user is owner of:', value=f'{is_owner_counter}', inline=False)
            traceEmbed.add_field(name='Number of server user has administrator permission in:', value=f'{is_admin_counter}', inline=False)
            traceEmbed.add_field(name='Number of servers user has manage server permission in:', value=f'{has_manageserver_counter}', inline=False)
            traceEmbed.add_field(name='Number of servers user has the top role in:', value=f'{has_toprole_counter}', inline=False)
            
            await interaction.response.send_message(embed=traceEmbed)
        else: await interaction.response.send_message('**UNEXPECTED ERROR: **Trace could not be completed at this time.', ephemeral=True)
    #----------------------------------------------------TRACE----------------------------------------------------#

    #----------------------------------------------------SERVER INFO----------------------------------------------------#
    @app_commands.command(name='server', description='Displays various server information')
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 60, key=lambda i: (i.guild))
    async def info_group_server(self, interaction: discord.Interaction):
        embedServerInfo = discord.Embed(
            title = f'DISPLAYING INFORMATION FOR {interaction.guild.name}',
            description = '*All times are being displayed in UTC Timezone.*',
            color = discord.Color.gold()
        ).set_thumbnail(url=interaction.guild.icon).set_footer(icon_url=interaction.user.avatar, text=f'Requested by: {interaction.user.name} | PROJECT UTOPIA™ by Insignia')
        embedServerInfo.add_field(name='Server Created On:', value=interaction.guild.created_at.strftime("%a, %#d %B %Y, %I:%M %p"))
        embedServerInfo.add_field(name='Server ID:', value=f'||{interaction.guild.id}||')
        embedServerInfo.add_field(name='Ownership Holder:', value=interaction.guild.owner.mention)
        embedServerInfo.add_field(name='Moderation Level:', value=str(interaction.guild.verification_level).upper())

        if interaction.guild.afk_channel: embedServerInfo.add_field(name='AFK Channel:', value=interaction.guild.afk_channel.mention)
        else: embedServerInfo.add_field(name='AFK Channel:', value='No AFK channel set in this server!')
        
        embedServerInfo.add_field(name='Number of Members:', value=interaction.guild.member_count)
        embedServerInfo.add_field(name='Number of Categories', value=len(interaction.guild.categories))
        embedServerInfo.add_field(name='Number of Roles:', value=len(interaction.guild.roles))
        embedServerInfo.add_field(name='Number of Text Channels:', value=len(interaction.guild.text_channels))
        embedServerInfo.add_field(name='Number of Voice Channels:', value=len(interaction.guild.voice_channels))
        embedServerInfo.add_field(name='Number of Emojis:', value=len(interaction.guild.emojis))
        embedServerInfo.add_field(name='Number of Boosts:', value=interaction.guild.premium_subscription_count)
        embedServerInfo.add_field(name='Boost Level:', value=interaction.guild.premium_tier)
        
        if interaction.guild.premium_subscribers != []: boosters = ", ".join([booster.mention for booster in interaction.guild.premium_subscribers])
        else: boosters = False
        
        if boosters: embedServerInfo.add_field(name='Boosters:', value=boosters)
        else: embedServerInfo.add_field(name='Boosters:', value='There are currently no boosters in the server!')

        bots_list = [bot.mention for bot in interaction.guild.members if bot.bot]
        embedServerInfo.add_field(name='Bots List', value=(", ".join(bots_list)))

        await interaction.response.send_message(embed=embedServerInfo)
        #----------------------------------------------------SERVER INFO----------------------------------------------------#

async def setup(client: commands.Bot):
    await client.add_cog(Trace(client), guilds=[discord.Object(id=)]) #Enter your server ID here
