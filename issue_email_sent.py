# Set the body of the message
body = u'''
<div style="margin:0px auto;text-align:center;font-size:12px;color:#a2a2a2;padding-bottom:6px">
  ## Por favor responde por encima de ésta línea .##
</div>
<div style="text-align:right;padding:8px 14px 0 0">
    <a href="http://www.vauxoo.com/" target="_blank"><img src="https://s3.amazonaws.com/s3.vauxoo.com/logopaypal.png" width="269" height="auto" alt="Harvest Support" style="border:0"></a>
</div>
<div "style=display: table;border-collapse: separate;border-spacing: 2px;border-color: gray;">
<p>Estimado cliente,</p>
<p> Este es un mensaje generado automáticamente </p>
<p>Acabo de abrir su <b>Ticket Referencia #{identifier}</b> y estoy por comenzar a trabajar en él. </p>
<p>Para ayudarnos a encontrar una solución, por favor proporcione, si no es que ya lo hizo, cualquier información adicional que sea útil, como por ejemplo:</p>
<ul>
<li>Pasos detallados para reproducir. <sup>1</sup></li>
<li>Un vídeo de corta duración y / o capturas de pantalla. <sup>2</sup></li>
<li>Toda la información pertinente acerca de su sistema y caso de uso para reproducir la falla o el caso de estudio. <sup>3</sup></li>
</ul>
<p>Dicha información la puedes pasar solo respondiendo éste correo electrónico.</p>
</div>
<p>Saludos cordiales, </p>
<ul style="list-style:none">
<li><sup>1</sup> <a href="http://es.wikipedia.org/wiki/Captura_de_pantalla">Herramientas para capturar pantalla</a></li>
<li><sup>2</sup> <a href="http://es.wikipedia.org/wiki/Screencast">Herramientas para hacer screencast</a></li>
<li><sup>3</sup> <a href="http://es.wikipedia.org/wiki/Caso_de_uso">Describir correctamente un caso de uso</a></li>
</ul>
'''.format(identifier = object.id)
subject = u'RE: ' + object.name
parents = [o.id for o in object.message_ids if o.type=='email']
parents.sort()
parent_id = parents and parents[0] or False

# Ordering in reverse to ensure NEVER send an email twice.

parents.sort(reverse=True)

message_obj = self.pool['mail.message']
sent_messages = message_obj.search(cr, uid, [('id', '=', parents[0])])
if sent_messages:
    message_obj.browse(cr, uid, sent_messages).body.find('acerca de su sistema y caso de uso para reproducir la falla o el caso de estudio') >= 0


# Put "uid" or your algorithm to search the new uid instead if you want the message to be sent by the current user.

self.message_post(cr, object.user_id.id, object.id, body=body, subject=subject, type='email', subtype='mail.mt_comment',
context=context, parent_id=parent_id, partner_ids=[object.partner_id.id])
