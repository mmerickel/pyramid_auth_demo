<%inherit file='base.mako' />

<p><a href="${ request.route_url('home') }">Home</a></p>
<p>Create a page <a href="${ request.route_url('create_page') }">here</a></p>

<h1>All Pages</h1>
% for page in pages:
<p><a href="${ request.route_url('page', title=page.uri) }">${ page.title }</a></p>
% endfor
