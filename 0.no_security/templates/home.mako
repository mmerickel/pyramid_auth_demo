<%inherit file='base.mako' />

% if user:
<p>You are logged in as: ${ user.login }</p>
<p><a href="${ request.route_url('logout') }">Logout</a></p>
% else:
<p>You are not logged in!</p>
<p><a href="${ request.route_url('login') }">Login</a></p>
% endif

<h2>Your Pages</h2>
% for page in user_pages:
<p>
    <a href="${ request.route_url('page', title=page.uri) }">${ page.title }</a>
</p>
% else:
<p>You have not created any pages.</p>
% endfor
