import psycopg2
from dotenv import load_dotenv
import os
from datetime import datetime,timedelta
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tabulate import tabulate



def weekly_email_func():
    load_dotenv()

    # print(os.getenv('hostname'))
    hostname=os.getenv('hostname')
    database=os.getenv('database')
    user_name=os.getenv('user_name')
    pwd=os.getenv('pwd')
    port_id=os.getenv('port_id')
   
    connection  = psycopg2.connect(user=user_name,
                password=pwd,
                database=database,
                host=hostname,
                port=port_id)

    cur=connection.cursor()
    today_date=datetime.today().date()
    six_days_ago=today_date-timedelta(days=6)

    #top 5 songs by listened duration in minutes
    top_5_songs_min=[['song_name','time(min)']]
    cur.callproc('top_5song_last_7days_func')
    for row in cur.fetchall():
        song_name=row[0]
        time_listened=float(row[1])
        element=[song_name,time_listened]
        top_5_songs_min.append(element)
    print(top_5_songs_min)

    #total duration played
    cur.callproc('total_time_played')
    total_duration_hrs=float(cur.fetchone()[0])
    print(total_duration_hrs)

    #top 5 songs and artist name
    top_5_songs_artist_played=[['Song Name','Artist Name','Times played']]
    cur.callproc('most_popular_song_artist_func')
    for row in cur.fetchall():
        song_name=row[0]
        artist_name=row[1]
        time_listened=row[2]
        element=[song_name,artist_name,time_listened]
        top_5_songs_artist_played.append(element)
  
    #top_artist_played
    top_artist_played=[['Artist name','Times Played']]
    cur.callproc('top_artist_func')
    for row in cur.fetchall():
        artist_name=row[0]
        times_played=int(row[1])
        element=[artist_name,times_played]
        top_artist_played.append(element)

    #top decade
    top_decade_played=[['Decade','Times Played']]
    cur.callproc('total_plays_by_decade_func')
    for row in cur.fetchall():
        decade=row[0]
        times_played=int(row[1])
        element=[decade,times_played]
        top_decade_played.append(element)

    #sending mail

    passcode="yffaobvxjxgqplcx"
    sender_email="sadichhya.maharjan@gmail.com"
    receiver_email='sadichhya.maharjan64@gmail.com'

    # message = MIMEMultipart("alternative")
    # message["Subject"] = f"Spotify - Weekly Roundup - {today_date}"
    # message["From"] = sender_email
    # message["To"] = receiver_email

    # text=f"""\
    #     Here are your stats for your weekly round up for Spotify. 
    #     Dates included: {six_days_ago} - {today_date}:

    #     Total Time Listened: {total_duration_hrs} hours.
    #     You listened to these songs and artists a lot here are your top 5!
    #     {top_5_songs_artist_played}
    #     You spent the most time listening to these songs:
    #     {top_5_songs_min}
    #     You spend the most time listening to these artists:
    #     {top_artist_played}
    #     Lastly your top decades are as follows:
    #     {top_decade_played}
    # """

    # html=f"""\
    # <html>
    #     <body>
    #         <h4>
    #         Here are your stats for your weekly round up for Spotify.
    #         </h4>
    #         <p>
    #         Dates included: {six_days_ago} - {today_date}
    #         <br>
    #         Total Time Listened: {total_duration_hrs} hours.
    #         <br>
    #         <h4>
    #         You listened to these songs and artists a lot here are your top 5!
    #         </h4>
    #         {tabulate(top_5_songs_artist_played, tablefmt='html')}
    #         <h4>
    #         You spend a lot of time listening to these songs!
    #         </h4>
    #         {tabulate(top_5_songs_min, tablefmt='html')}
    #         <h4>
    #         You spend a lot of time listening to these artists!
    #         </h4>
    #         {tabulate(top_artist_played, tablefmt='html')}
    #         <h4>
    #         Lastly your top decades are as follows:
    #         </h4>
    #         {tabulate(top_decade_played, tablefmt='html')}
    #         </p>
    #     </body>
    # </html>"""

    # text_part=MIMEText(text,"plain")
    # html_part=MIMEMultipart(html,"html")

    # message.attach(text_part)
    # message.attach(html_part)

    # context = ssl.create_default_context()
    # with smtplib.SMTP_SSL("smtp.gmail.com",465,context = context) as server:
    #     server.login(sender_email,passcode)
    #     server.sendmail(sender_email,receiver_email,message.as_string())
    # return "Email Sent"



    message = MIMEMultipart('alternative')
    message["Subject"] = f"Spotify - Weekly Roundup - {today_date}"
    message["From"] = sender_email
    message["To"] = receiver_email
    text = f"""\
    Here are your stats for your weekly round up for Spotify. 
    Dates included: {six_days_ago} - {today_date}:
    
    Total Time Listened: {total_duration_hrs} hours.
    You listened to these songs and artists a lot here are your top 5!
    {top_5_songs_artist_played}
    You spent the most time listening to these songs:
    {top_5_songs_min}
    You spend the most time listening to these artists:
    {top_artist_played}
    """
    html = f"""\
    <html>
        <body>
            <h4>
            Here are your stats for your weekly round up for Spotify.
            </h4>
            <p>
            Dates included: {six_days_ago} - {today_date}
            <br>
            Total Time Listened: {total_duration_hrs} hours.
            <br>
            <h4>
            You listened to these songs and artists a lot here are your top 5!
            </h4>
            {tabulate(top_5_songs_artist_played, tablefmt='html')}
            <h4>
            You spend a lot of time listening to these songs!
            </h4>
            {tabulate(top_5_songs_min, tablefmt='html')}
            <h4>
            You spend a lot of time listening to these artists!
            </h4>
            {tabulate(top_artist_played, tablefmt='html')}
            </p>
        </body>
    </html>"""
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, passcode)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


weekly_email_func()
   