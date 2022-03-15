{% macro pad_row(cols) -%}
    {% for i in range(cols) %}
        <td class="pad"></td>
    {% endfor %}
{%- endmacro %}

<table>
<thead>
<tr>
    <th>Time</th>
    {% for i in range(1, day["max_parallel_sessions"]+1) %}
        <th>Track {{ i }}</th>
    {%  endfor %}
</tr>
</thead>
<tbody>

{%  for block in day["blocks"] %}
    <tr>
        <td></td>
        {%-  for sess in block._parallel_sessions %}
            <td>{{ sess.name }}</td>
            {%  if loop.last %}
                {{ pad_row(day["max_parallel_sessions"]-loop.length) }}
            {%  endif %}
        {%-  endfor -%}
    </tr>
    {%  for slot in block.slots %}
    <tr>
        <td>{{ slot.start }} -- {{ slot.end }}</td>
        {%-  for talk in slot.talks %}

            <td>
            <div class="talk">
                <h1>
                    {%  if talk.link %}
                    <a href="{{ talk.link }}">
                    {%  endif %}
                    {{ talk.title }}
                    {%  if talk.link %}
                    </a>
                    {%  endif %}
                </h1>
                <h2>
                    {%  if talk.contact %}
                        <a href="mailto:{{ talk.contact }}">
                    {%  endif %}
                    {{ talk.speaker }}
                    {%  if talk.contact %}
                        </a>
                    {%  endif %}
                </h2>
                <p>{{ talk.description }}</p>
            </div>
            </td>
            {%  if loop.last %}
                {{ pad_row(day["max_parallel_sessions"]-loop.length) }}
            {%  endif %}
        {% else %}
            <td><div class="pause">Pause {{ slot.pause }}</div></td>
            {{ pad_row(day["max_parallel_sessions"]-1) }}
        {%-  endfor -%}

    </tr>
    {%  endfor %}

{% endfor %}

</tbody>
</table>
