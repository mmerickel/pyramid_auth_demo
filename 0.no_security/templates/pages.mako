<%inherit file='base.mako' />

<h1>All Pages</h1>
% for page in pages:
<p><a href="${ request.route_url('page', title=page.uri) }">${ page.title }</a></p>
% endfor
