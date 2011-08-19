<%inherit file='base.mako' />

<h1>Admin View</h1>
<p>Congratulations, if you're here you're an admin!</p>

<h2>All users:</h2>
<table>
% for k, v in users.items():
    <tr><td>${ k }</td><td>${ v }</td></tr>
% endfor
</table>
