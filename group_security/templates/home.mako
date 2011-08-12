<%inherit file='base.mako' />

<h1>Hello World!</h1>
% if user:
<p>You are logged in as: ${ user }</p>
<p><a href="${ request.route_url('logout') }">Logout</a></p>
% else:
<p>You are not logged in!</p>
<p><a href="${ request.route_url('login') }">Login</a></p>
% endif
<p>
    Click <a href="${ request.route_url('secure') }">here</a>
    to see a secure view.
</p>
<p>
    Click <a href="${ request.route_url('admin') }">here</a>
    to see the admin view.
</p>
