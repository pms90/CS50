select title from movies
join stars as s1 on movies.id = s1.movie_id
join people as p1 on s1.person_id = p1.id and p1.name = 'Johnny Depp'
join stars as s2 on movies.id = s2.movie_id
join people as p2 on s2.person_id = p2.id and p2.name = 'Helena Bonham Carter';