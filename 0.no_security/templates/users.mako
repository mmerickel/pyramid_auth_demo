<%inherit file='base.mako' />

<h1>All Users</h1>
% for login in users:
<p><a href="${ request.route_url('user', login=login) }">${ login }</a></p>
% endfor
