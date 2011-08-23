<%inherit file='base.mako' />

<p>Click <a href="${ request.route_url('edit_page', title=page.uri) }">here</a> to edit this page.</p>

<h1>${ page.title }</h1>
<p>Owner: <a href="${ request.route_url('user', login=page.owner) }">${ page.owner }</a></p>
<p>Body:</p>
<div style="margin-left: 4em;">
    ${ page.body | n }
</div>
