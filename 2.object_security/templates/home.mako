<%inherit file='base.mako' />

% if user:
<p>You are logged in as: <a href="${ request.route_url('user', login=user.login) }">${ user.login }</a></p>
<p><a href="${ request.route_url('logout') }">Logout</a></p>
% else:
<p>You are not logged in!</p>
<p><a href="${ request.route_url('login') }">Login</a></p>
% endif

<p>Create a page <a href="${ request.route_url('create_page') }">here</a></p>

<p><a href="${ request.route_url('pages') }">All Pages</a></p>
<p><a href="${ request.route_url('users') }">All Users</a></p>

<h2>Your Pages</h2>
% if user_pages:
% for page in user_pages:
<p>
    <a href="${ request.route_url('page', title=page.uri) }">${ page.title }</a>
</p>
% endfor
% else:
<p>You have not created any pages.</p>
% endif
