<%inherit file='base.mako' />

<h1>Hello World!</h1>
% if user:
<p>You are logged in as: ${ user }</p>
<p>
    Click <a href="${ request.route_url('user', login=user) }">here</a>
    to see your credentials.
</p>
<p><a href="${ request.route_url('logout') }">Logout</a></p>
% else:
<p>You are not logged in!</p>
<p><a href="${ request.route_url('login') }">Login</a></p>
% endif
<p>
    Click <a href="${ request.route_url('users') }">here</a>
    to see a list of users.
</p>
