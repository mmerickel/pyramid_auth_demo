<%inherit file='base.mako' />

% for u in users:
<p><a href="${ request.route_url('user', login=u) }">${ u }</a></p>
% endfor
