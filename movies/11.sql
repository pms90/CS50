select title from movies
inner join ratings r on movies.id = r.movie_id
inner join stars s on movies.id = s.movie_id
inner join people p on s.person_id = p.id
where p.name = 'Chadwick Boseman'
order by r.rating desc
limit 5;