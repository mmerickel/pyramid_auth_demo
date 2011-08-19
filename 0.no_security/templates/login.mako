<%inherit file='base.mako' />

% if failed_attempt:
<p><font color="red">Invalid credentials, try again.</font></p>
% endif
<form method="post" action="${ request.path }">
    <p>
        <label for="login">Login</label><br>
        <input type="text" name="login" value="${ login }">
    </p>
    <p>
        <label for="passwd">Password</label><br>
        <input type="password" name="passwd">
    </p>
    <input type="hidden" name="next" value="${ next }">
    <input type="submit" name="submit">
</form>

<h3>Valid login / password combinations:</h3>
% for k, v in users.items():
<p>${ k } / ${ v.password }</p>
% endfor
