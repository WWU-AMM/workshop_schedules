{%  for day in days %}
Day start: {{ day["start"] }}
    Blocks:
    {%  for block in day["blocks"] %}
        Slots:
        {%  for slot in block.slots %}
            - {{ slot.start }} -- {{ slot.end }}
            Sessions {%-  for sess in block._parallel_sessions %}
                {{ sess.name }}
            {%-  endfor -%}
        {%  endfor %}
    {%  endfor %}
{%  endfor %}
