select p.name from people p
join stars s1 on p.id = s1.person_id
join stars s2 on s1.movie_id = s2.movie_id
join people p2 on s2.person_id = p2.id
join movies m on s1.movie_id = m.id
where p2.name = 'Kevin Bacon' and p.name != 'Kevin Bacon' and p2.birth = 1958;

