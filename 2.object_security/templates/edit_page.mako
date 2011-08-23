<%inherit file='base.mako' />

% if errors:
<ul>
    % for e in errors:
    <li>${ e }</li>
    % endfor
</ul>
% endif
<form method="post" action="${ request.path }">
    <h3>Title</h3>
    <input type="text" name="title" value="${ title }"/>
    <h3>Owner</h3>
    <h4>${ owner }</h4>
    <h3>Body</h3>
    <textarea name="body" rows="10" columns="60">${ body }</textarea>
    <br/>
    <input type="submit" name="submit" value="Submit"/>
</form>
