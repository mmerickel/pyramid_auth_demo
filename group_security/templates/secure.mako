<%inherit file='base.mako' />

<h1>Secure View</h1>
<p>Welcome to the secure view, you're authenticated!</p>

<p>User: ${ user }</p>
<p>Groups: ${ ', '.join(groups) }</p>
