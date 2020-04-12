# Notes on celery

These should now work ipython, after activating rabbitmq broker and pg backend


	inner_chord1 = chord([mul.s(2, 3), mul.s(3, 4)], tsum.s())

	inner_chord2 = chord([mul.s(4, 5), mul.s(5, 6)], tsum.s())

	outer_chord = group(inner_chord1, inner_chord2) | tsum.s()

	outer_chord()
