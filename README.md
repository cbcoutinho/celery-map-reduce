# Notes on celery


These should now work IPython, after activating RabbitMQ broker and PostgreSQL
backend


	inner_chord1 = chord([multiply.s(2, 3), multiply.s(3, 4)], reducer.s())

	inner_chord2 = chord([multiply.s(4, 5), multiply.s(5, 6)], reducer.s())

	outer_chord = group(inner_chord1, inner_chord2) | reducer.s()

	outer_chord()
	
[sample.png](https://i.stack.imgur.com/PsWEF.png)
