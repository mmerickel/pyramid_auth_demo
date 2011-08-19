<%inherit file='base.mako' />

<h1>User Information</h1>
<p>Login: ${ user.login }</p>
<p>Password: ${ user.password }</p>
<p>Groups: ${ ', '.join(user.groups) }</p>
<p>Pages:</p>
<div style="margin-left: 4em;">
% for page in pages:
    <p><a href="${ request.route_url('page', title=page.uri) }">${ page.title }</a></p>
% endfor
</div>
