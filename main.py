import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import re
from datetime import timedelta
import sqlite3

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Database setup
def init_db():
    conn = sqlite3.connect('warnings.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS warnings (
            user_id INTEGER,
            guild_id INTEGER,
            warning_count INTEGER,
            PRIMARY KEY (user_id, guild_id)
        )
    ''')
    conn.commit()
    conn.close()

def get_warnings(user_id, guild_id):
    conn = sqlite3.connect('warnings.db')
    cursor = conn.cursor()
    cursor.execute('SELECT warning_count FROM warnings WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def add_warning(user_id, guild_id):
    conn = sqlite3.connect('warnings.db')
    cursor = conn.cursor()
    current = get_warnings(user_id, guild_id)
    cursor.execute('INSERT OR REPLACE INTO warnings (user_id, guild_id, warning_count) VALUES (?, ?, ?)', 
                   (user_id, guild_id, current + 1))
    conn.commit()
    conn.close()
    return current + 1

def reset_warnings(user_id, guild_id):
    conn = sqlite3.connect('warnings.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM warnings WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
    conn.commit()
    conn.close()

# Promotion patterns
PROMO_PATTERNS = [
    r'(?:http|www|bit\.ly|discord\.gg)',
    r'(?:check out|click here|buy now|visit|subscribe)',
    r'(?:my server|my bot|my project|my website|my channel)',
    r'(?:promo code|discount|affiliate|ref code)',
    r'(?:dm me|dm for|dm to)',
]

BLOCKED_DOMAINS = [
    'twitch.tv', 'youtube.com', 'tiktok.com',
    'patreon.com', 'kickstarter.com', 'gofundme.com',
    'amazon.com', 'etsy.com',
]

def is_advertisement(message_content):
    content = message_content.lower()
    
    for pattern in PROMO_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            return True
    
    for domain in BLOCKED_DOMAINS:
        if domain in content:
            return True
    
    return False

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    init_db()
    print('Database initialized')

@bot.event
async def on_message(message):
    if message.author.bot:
        await bot.process_commands(message)
        return
    
    if message.author.guild_permissions.administrator or message.author.guild_permissions.moderate_members:
        await bot.process_commands(message)
        return
    
    if is_advertisement(message.content):
        user_id = message.author.id
        guild_id = message.guild.id
        
        # Delete the message
        try:
            await message.delete()
        except discord.Forbidden:
            pass
        
        # Increment warnings
        warnings = add_warning(user_id, guild_id)
        
        if warnings == 1:
            embed = discord.Embed(
                title="⚠️ Warning: Advertisement Detected",
                description=f"Hello {message.author.mention},\n\nYour message was removed because it contains self-promotion or advertising.\n\nThis is your **first warning**. Please avoid promotional content.",
                color=discord.Color.yellow()
            )
            embed.set_footer(text="Further violations may result in mute or ban.")
            
            try:
                await message.author.send(embed=embed)
            except:
                pass
            
            warning_msg = await message.channel.send(
                f"{message.author.mention} Your message was removed for containing advertisement. This is your first warning."
            )
            await warning_msg.delete(delay=10)
        
        elif warnings == 2:
            embed = discord.Embed(
                title="⚠️ Second Warning: Advertisement",
                description=f"Hello {message.author.mention},\n\nThis is your **second warning**. Further violations will result in a mute.",
                color=discord.Color.orange()
            )
            
            try:
                await message.author.send(embed=embed)
            except:
                pass
            
            warning_msg = await message.channel.send(
                f"{message.author.mention} Second warning for advertisement. Next violation = mute."
            )
            await warning_msg.delete(delay=10)
        
        elif warnings >= 3:
            embed = discord.Embed(
                title="🔇 Muted: Excessive Advertising",
                description=f"Hello {message.author.mention},\n\nYou have been **muted for 24 hours** due to repeated advertisement violations.",
                color=discord.Color.red()
            )
            
            try:
                await message.author.send(embed=embed)
            except:
                pass
            
            try:
                await message.author.timeout(timedelta(hours=24), reason="Repeated advertisement violations")
                mute_msg = await message.channel.send(
                    f"{message.author.mention} has been muted for 24 hours due to repeated advertising."
                )
                await mute_msg.delete(delay=10)
            except discord.Forbidden:
                warning_msg = await message.channel.send(
                    f"{message.author.mention} I don't have permission to mute you, but you've violated the rules multiple times."
                )
                await warning_msg.delete(delay=10)
            
            reset_warnings(user_id, guild_id)
    
    await bot.process_commands(message)

@bot.command(name="warnings")
@commands.has_permissions(moderate_members=True)
async def check_warnings(ctx, user: discord.User):
    """Check warning count for a user (mod command)"""
    warnings = get_warnings(user.id, ctx.guild.id)
    embed = discord.Embed(
        title=f"Warnings for {user.name}",
        description=f"{user.mention} has **{warnings}** advertisement warnings.",
        color=discord.Color.blurple()
    )
    await ctx.send(embed=embed)

@bot.command(name="reset_warnings")
@commands.has_permissions(moderate_members=True)
async def reset_warnings_cmd(ctx, user: discord.User):
    """Reset warnings for a user (mod command)"""
    reset_warnings(user.id, ctx.guild.id)
    await ctx.send(f"✅ Warnings reset for {user.mention}.")

bot.run(TOKEN)
