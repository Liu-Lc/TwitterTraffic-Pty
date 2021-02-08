DELETE FROM tweets
	WHERE text ~* 'san carlos|capira|veraguas|coronado|chitré|penonom[eé]|cocl[eé]|pacora' 
		or text ~* 'bocas del toro|chiriqu[ií]|boquete|chepo|río hato|chame';

DELETE FROM tweets
	WHERE text ~* 'aguadulce|las tablas|los santos|chitr[eé]|[^\w]ant[oó]n[^\w]|campana'

delete from tweets
	where text !~* 'panam[aá].{0,5}col[oó]n|direcci[oó]n.{0,15}col[oó]n|direcci[oó]n.{0,10}provincia.{0,5}col[oó]n'
		and text ~* 'col[oó]n';

UPDATE public.tweets
	SET place=0
	WHERE text ~* 'howard'
		and text !~* 'direcci[oó]n (a|hacia) howard';

UPDATE public.tweets
	SET place=1
	WHERE text ~* 'loma co[vb][áa]'
		and text !~* 'direcci[oó]n (a|hacia) loma co[vb][áa]';

UPDATE public.tweets
	SET place=2
	WHERE text ~* 'burunga'
		and text ~* 'centenario'
		and text !~* 'direcci[oó]n (a|hacia) burunga';

UPDATE public.tweets
	SET place=3
	WHERE text ~* 'burunga'
		and text ~* 'interamericana|panamericana'
		and text !~* 'direcci[oó]n (a|hacia) burunga';

alter table public.place add column street text, 
	add column town text, 
	add column district text;


update tweets set place=null;

alter table tweets alter column place type bigint using place::bigint;

alter table locations add constraint pk_locations_id primary key(index);
alter table tweets add constraint fk_place_id foreign key(place)
	references locations(index);



UPDATE public.tweets
	SET place=4
	WHERE text ~* 'power[ ]*club'
		and text ~* 'ricardo.*alfaro|tumba muerto';
		
UPDATE public.tweets
	SET place=5
	WHERE text ~* 'banco nacional'
		and text ~* 'ricardo.*alfaro|tumba muerto'; 
		
UPDATE public.tweets
	SET place=6
	WHERE text ~* 'price[ ]*smart'
		and text ~* 'ricardo.*alfaro|tumba muerto'; 

UPDATE public.tweets
	SET place=7
	WHERE text ~* 'mc[ ]*donald'
		and text ~* 'ricardo.*alfaro|tumba muerto'; 
		
UPDATE public.tweets
	SET place=8
	WHERE text ~* 'do[ ]*it[ ]*center'
		and text ~* 'ricardo.*alfaro|tumba muerto'; 
		
UPDATE public.tweets
	SET place=9
	WHERE text ~* '99'
		and text ~* 'ricardo.*alfaro|tumba muerto'; 
		
UPDATE public.tweets
	SET place=10
	WHERE text ~* 'migraci[oó]'
		and text ~* 'ricardo.*alfaro|tumba muerto'; 
		
UPDATE public.tweets
	SET place=11
	WHERE text ~* 'universidad latina'
		and text ~* 'ricardo.*alfaro|tumba muerto'; 
		
UPDATE public.tweets
	SET place=12
	WHERE text ~* 'usma'
		and text ~* 'ricardo.*alfaro|tumba muerto';

UPDATE public.tweets
	SET place=20
	WHERE text ~* 'dorado'
	and text !~* 'direcci[oó]n (a|al|hacia|hacia el|a el) dorado'
		and place is null;

UPDATE tweets SET place=21 
                         WHERE text ~* 'hospital'
                          AND text ~* 'ricardo.*alfaro|tumba muerto';

UPDATE tweets SET place=22 
                         WHERE text ~* 'machetazo'
                          AND text ~* 'ricardo.*alfaro|tumba muerto|miguelito';

UPDATE tweets SET place=23 
                         WHERE text ~* 'machetazo'
                          AND text ~* 'calidonia|(avenida )* perú';

UPDATE tweets SET place=24 
                         WHERE text ~* 'machetazo'
                          AND text ~* 'tocumen|24 de diciembre|panamericana|interamericana|corredor norte|mañanitas';
UPDATE tweets SET place=25 
                         WHERE text ~* 'machetazo'
                          AND text ~* 'hato montaña';
UPDATE tweets SET place=26 
                         WHERE text ~* 'machetazo'
                          AND text ~* 'versalles';
UPDATE tweets SET place=27 
                         WHERE text ~* 'machetazo'
                          AND text ~* 'costa sur|corredor sur';
UPDATE tweets SET place=28 
                         WHERE text ~* 'juan pablo'
                          AND text ~* 'corredor|ricardo.*alfaro|tumba muerto|locer[ií]a|trans[ií]s(t)*mica|plaza edison' AND text !~* '(río|barriada) juan pablo';
UPDATE tweets SET place=29 
                         WHERE text ~* 'juan pablo'
                          AND text ~* 'metropolitano' AND text !~* '(río|barriada) juan pablo';
UPDATE tweets SET place=30 
                         WHERE text ~* 'juan pablo'
                          AND text ~* 'universidad' AND text !~* '(río|barriada) juan pablo';
UPDATE tweets SET place=31 
                         WHERE text ~* 'juan pablo|la amistad'
                          AND text ~* 'albrook' AND text !~* '(río|barriada) juan pablo';

UPDATE public.tweets
	SET place=32
	WHERE text ~* 'albrook' and text ~* 'corredor\s'
	and text !~* 'hasta albrook|dirección(.{0,10})albrook|direcci[oó]n(.{0,10})corredor'
		and place is null;

UPDATE tweets SET place=33 
		WHERE place is null AND text ~* 'altura(.{0,8})puente'
		AND text ~* 'puente(.{0,10})am[eé]ricas';
UPDATE tweets SET place=34 
		WHERE place is null AND text ~* 'altura(.{0,8})arraij[aá]n'
		AND text ~* 'puente(.{0,10})am[eé]ricas|cabecera' AND text !~* 'dirección(.{0,10})arraiján';