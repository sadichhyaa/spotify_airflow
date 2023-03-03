--top 5 songs played in last 7 days
select st.song_name, round((sum(st.song_duration)/60000),2) as song_duration_min
from spotify_schema.spotify_tracks as st
where st.song_played_at>current_date-interval '7 days' 
group by st.song_name
order by song_duration_min desc limit 5;

--creating function that returns top 5 songs 
Create function top_5song_last_7days_func ()
Returns table(song_name text,song_duration_min decimal) LANGUAGE plpgsql as $$
BEGIN
	return query
	select st.song_name, round((sum(st.song_duration)/60000),2) as song_duration_min
	from spotify_schema.spotify_tracks as st
	where st.song_played_at>current_date-interval '7 days' 
	group by st.song_name
	order by song_duration_min desc limit 5;
end;$$

--total duration

select  round((sum(st.song_duration)/3600000),2) as total_time_listened_hrs
from spotify_schema.spotify_tracks as st
where st.song_played_at>current_date-interval '7 days'; 

--function
Create function total_time_played ()
Returns table(total_time_listened_hrs decimal) LANGUAGE plpgsql as $$
BEGIN
	return query
	select  round((sum(st.song_duration)/3600000),2) as total_time_listened_hrs
	from spotify_schema.spotify_tracks as st
	where st.song_played_at>current_date-interval '7 days';
end;$$


--most populat song_name and artist_name

select st.song_name,sa.name as artist_name, count(st.*) as times_played
from spotify_schema.spotify_tracks as st 
inner join
spotify_schema.spotify_artists as sa
on st.artist_id=sa.artist_id
where st.song_played_at>current_date-interval '7 days'
group by st.song_name,sa.name
order by times_played desc limit 5;

Create function most_popular_song_artist_func ()
Returns table(song_name text,artist_name text, times_played int) LANGUAGE plpgsql as $$
BEGIN
	return query
	select st.song_name,sa.name as artist_name, count(st.*) as times_played
	from spotify_schema.spotify_tracks as st 
	inner join
	spotify_schema.spotify_artists as sa
	on st.artist_id=sa.artist_id
	where st.song_played_at>current_date-interval '7 days'
	group by st.song_name,sa.name
	order by times_played desc limit 5;
end;$$

--top artist

select sa.name as artist_name, count(st.*) as number_plays
from spotify_schema.spotify_tracks as st 
inner join
spotify_schema.spotify_artists as sa
on st.artist_id=sa.artist_id
where st.song_played_at>current_date-interval '7 days'
group by sa.name
order by number_plays desc limit 5;

Create function top_artist_func ()
Returns table(artist_name text, number_plays int) LANGUAGE plpgsql as $$
BEGIN
	return query
	select sa.name as artist_name, count(st.*) as number_plays
	from spotify_schema.spotify_tracks as st 
	inner join
	spotify_schema.spotify_artists as sa
	on st.artist_id=sa.artist_id
	where st.song_played_at>current_date-interval '7 days'
	group by sa.name
	order by number_plays desc limit 5;
end;$$


--decade view (album released decades)

create or replace view track_decade as
select *,
case
WHEN subqry.release_year >= 1950 AND subqry.release_year <= 1959  THEN '1950''s'
WHEN subqry.release_year >= 1960 AND subqry.release_year <= 1969  THEN '1960''s'
WHEN subqry.release_year >= 1970 AND subqry.release_year <= 1979  THEN '1970''s'
WHEN subqry.release_year >= 1980 AND subqry.release_year <= 1989  THEN '1980''s'
WHEN subqry.release_year >= 1990 AND subqry.release_year <= 1999  THEN '1990''s'
WHEN subqry.release_year >= 2000 AND subqry.release_year <= 2009  THEN '2000''s'
WHEN subqry.release_year >= 2010 AND subqry.release_year <= 2019  THEN '2010''s'
WHEN subqry.release_year >= 2020 AND subqry.release_year <= 2029  THEN '2020''s'
WHEN subqry.release_year >= 2030 AND subqry.release_year <= 2039  THEN '2030''s'
WHEN subqry.release_year >= 2040 AND subqry.release_year <= 2049  THEN '2040''s'
ELSE 'Other'
END AS decade
from
(select sal.album_id,sal.name,sal.release_date,st.unique_id,st.song_name,st.song_played_at,cast(SPLIT_PART(sal.release_date,'-',1)as decimal) as release_year
 from spotify_schema.spotify_album as sal 
 inner join
 spotify_schema.spotify_tracks as st on sal.album_id=st.album_id) as subqry;


--total plays in each decade album
SELECT decade, COUNT(unique_id) AS total_plays
FROM track_decade
WHERE song_played_at > CURRENT_DATE - INTERVAL '7 days'
GROUP BY decade
ORDER BY total_plays DESC;


Create function total_plays_by_decade_func ()
Returns table(decade text, total_plays int) LANGUAGE plpgsql as $$
BEGIN
	return query
	SELECT decade, COUNT(unique_id) AS total_plays
	FROM track_decade
	WHERE song_played_at > CURRENT_DATE - INTERVAL '7 days'
	GROUP BY decade
	ORDER BY total_plays DESC;
end;$$
