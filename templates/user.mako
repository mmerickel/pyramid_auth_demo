<%inherit file='base.mako' />

<p>User: ${ login }</p>
<p>Groups: ${ ', '.join(groups) }</p>
