DELETE FROM public.to_sql_test
	WHERE text ~* 'san carlos|capira|veraguas|coronado|chitré|penonom[eé]|cocl[eé]|colón';

UPDATE public.to_sql_test
	SET place='Howard'
	WHERE text ~* 'howard'
		and text !~* 'direcci[oó]n (a|hacia) howard';

UPDATE public.to_sql_test
	SET place='Loma Cobá'
	WHERE text ~* 'loma co[vb][áa]'
		and text !~* 'direcci[oó]n (a|hacia) loma co[vb][áa]';

alter table public.place add column street text, 
	add column town text, 
	add column district text;

