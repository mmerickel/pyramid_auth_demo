<%inherit file='base.mako' />

<h1>${ title }</h1>
<p>Owner: <a href="${ request.route_url('user', login=owner) }">${ owner }</a></p>
<div class="page_body">
    ${ body }
</div>
