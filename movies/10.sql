select people.name
from people
inner join directors on directors.person_id = people.id
inner join ratings on ratings.movie_id = directors.movie_id
where ratings.rating >= 9.0;