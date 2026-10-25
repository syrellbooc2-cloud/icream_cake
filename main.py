# ==========================================================
# Ice Cream Cake - website logic (PyScript / MicroPython)
# Sections: data, helpers, menu, order cart, flavor picker, ad popup, start-up
# Ad video setting: change AD_VIDEO near the ad popup section.
# ==========================================================

from pyscript import document, when

PESO = "\u20b1"

FLAVOR_ORDER = ["chocolate", "vanilla", "strawberry", "ube", "mango"]
FLAVORS = {
    "chocolate": ("Chocolate", "Fudgy cocoa cake, chocolate ice cream, and a chocolate drip. Our most requested flavor.", 25),
    "vanilla": ("Vanilla", "Classic creamy vanilla ice cream between soft golden cake layers.", 6),
    "strawberry": ("Strawberry", "Sweet strawberry ice cream with light pink cake layers and a fruity finish.", 6),
    "ube": ("Ube", "A local favorite: purple yam ice cream with soft ube-colored cake layers.", 5),
    "mango": ("Mango", "Bright, sunny mango ice cream layered with soft cake.", 4),
}
TOTAL_VOTES = 46

SIZE_ORDER = ["small", "medium", "large", "custom"]
SIZES = {
    "small": ("Small", "6-inch", "Serves 4 to 6", 199, "Cake layers, ice cream, and toppings"),
    "medium": ("Medium", "8-inch", "Serves 8 to 10", 399, "Cake layers, ice cream, and toppings"),
    "large": ("Large", "10-inch", "Serves 12 to 15", 599, "Cake layers, ice cream, and toppings"),
    "custom": ("Customized Large", "10-inch", "Serves 12 to 15", 799, "Custom decorations and your own message"),
}


def q(selector):
    return document.querySelector(selector)


def money(n):
    s = str(n)
    out = ""
    while len(s) > 3:
        out = "," + s[-3:] + out
        s = s[:-3]
    return PESO + s + out


def render_menu():
    rows = ""
    for key in SIZE_ORDER:
        name, dia, serves, price, what = SIZES[key]
        rows += (
            '<li class="size-row">'
            '<div class="mini mini-' + key + '" aria-hidden="true"></div>'
            '<div class="size-info"><h3>' + name + ' cake</h3>'
            '<p>' + dia + ' cake. ' + serves + '.</p>'
            '<p>' + what + '.</p></div>'
            '<div class="size-buy"><span class="price">' + money(price) + '</span>'
            '<a class="btn small" id="pick-' + key + '" href="#order">Order this size</a></div>'
            '</li>'
        )
    q("#menu-list").innerHTML = rows


def render_options():
    sizes = ""
    for key in SIZE_ORDER:
        name, dia, serves, price, what = SIZES[key]
        sizes += '<option value="' + key + '">' + name + " (" + dia + ") - " + money(price) + "</option>"
    q("#size").innerHTML = sizes

    flavors = ""
    for key in FLAVOR_ORDER:
        flavors += '<option value="' + key + '">' + FLAVORS[key][0] + "</option>"
    q("#flavor").innerHTML = flavors


def render_bars():
    html = ""
    for key in FLAVOR_ORDER:
        name, blurb, votes = FLAVORS[key]
        pct = votes * 100 / TOTAL_VOTES
        label = "%.1f" % pct
        html += (
            '<div class="bar" data-flavor="' + key + '">'
            '<span>' + name + '</span>'
            '<span class="bar-track"><i style="width:' + label + '%"></i></span>'
            '<span class="bar-val">' + label + '%</span>'
            '</div>'
        )
    q("#bars").innerHTML = html


cart = []  # each item: [size_key, flavor_key, quantity]


def read_qty():
    try:
        qty = int(q("#qty").value)
    except ValueError:
        qty = 1
    if qty < 1:
        qty = 1
    if qty > 20:
        qty = 20
    return qty


def cart_totals():
    total = 0
    cakes = 0
    for item in cart:
        total += SIZES[item[0]][3] * item[2]
        cakes += item[2]
    return total, cakes


def make_remove_handler(index):
    def handler(event):
        cart.pop(index)
        update()
    return handler


def render_cart():
    if len(cart) == 0:
        q("#cart-list").innerHTML = '<li class="cart-empty">No cakes yet. Choose a size and flavor, then press Add to my order.</li>'
        return
    html = ""
    i = 0
    for item in cart:
        name, dia, serves, price, what = SIZES[item[0]]
        flavor_name = FLAVORS[item[1]][0]
        line = price * item[2]
        html += '<li class="cart-item">'
        html += '<div><strong>' + str(item[2]) + ' x ' + name + '</strong>'
        html += '<span>' + dia + ', ' + flavor_name + '</span></div>'
        html += '<span class="line-price">' + money(line) + '</span>'
        html += '<button type="button" class="remove" id="rm-' + str(i) + '" aria-label="Remove ' + name + ', ' + flavor_name + ' from my order">Remove</button>'
        html += '</li>'
        i += 1
    q("#cart-list").innerHTML = html
    for n in range(len(cart)):
        when("click", "#rm-" + str(n))(make_remove_handler(n))


def refresh(event=None):
    total, cakes = cart_totals()
    q("#total").textContent = money(total)
    if cakes == 0:
        q("#total-note").textContent = ""
        q("#summary").value = "Add a cake to your order and your message will appear here."
        return
    if cakes == 1:
        q("#total-note").textContent = "1 cake"
    else:
        q("#total-note").textContent = str(cakes) + " cakes"

    mode = q("#mode").value
    cust = str(q("#cust").value).strip()
    when_needed = str(q("#when").value).strip()
    note = str(q("#note").value).strip()

    lines = ["Hello Ice Cream Cake! I would like to order:", ""]
    has_custom = False
    for item in cart:
        name, dia, serves, price, what = SIZES[item[0]]
        flavor_name = FLAVORS[item[1]][0]
        lines.append("- " + str(item[2]) + " x " + name + " (" + dia + "), " + flavor_name + ": " + money(price * item[2]))
        if item[0] == "custom":
            has_custom = True
    lines.append("")
    lines.append("Estimated total: " + money(total))
    lines.append("Pickup or delivery: " + mode)
    if when_needed:
        lines.append("Date needed: " + when_needed)
    else:
        lines.append("Date needed: (please tell me what dates are available)")
    if cust:
        lines.append("Name: " + cust)
    if note:
        lines.append("Message or design notes: " + note)
    elif has_custom:
        lines.append("Message or design notes: (I will share my design idea)")
    lines.append("")
    lines.append("Thank you!")
    q("#summary").value = "\n".join(lines)


def update(event=None):
    render_cart()
    refresh()


def add_cake(event):
    size_key = q("#size").value
    flavor_key = q("#flavor").value
    if size_key not in SIZES or flavor_key not in FLAVORS:
        return
    qty = read_qty()
    merged = False
    for item in cart:
        if item[0] == size_key and item[1] == flavor_key:
            item[2] = min(item[2] + qty, 20)
            merged = True
    if not merged:
        cart.append([size_key, flavor_key, qty])
    q("#add-status").textContent = "Added " + str(qty) + " x " + SIZES[size_key][0] + ", " + FLAVORS[flavor_key][0] + ". Pick another size or flavor to add more."
    update()


def set_flavor(key):
    name, blurb, votes = FLAVORS[key]
    q("#stage").setAttribute("data-flavor", key)
    q("#flavor-name").textContent = name
    q("#flavor-blurb").textContent = blurb
    for k in FLAVOR_ORDER:
        if k == key:
            q("#btn-" + k).setAttribute("aria-pressed", "true")
        else:
            q("#btn-" + k).setAttribute("aria-pressed", "false")
    q("#flavor").value = key


def make_flavor_handler(key):
    def handler(event):
        set_flavor(key)
    return handler


def make_size_handler(key):
    def handler(event):
        q("#size").value = key
    return handler


def select_message(event):
    box = q("#summary")
    box.focus()
    box.select()


# ---------- Ad popup ----------
# AD_VIDEO: leave "" for the built-in slideshow, or use a video file name (ad.mp4),
# or paste a YouTube link (watch, youtu.be, shorts and embed links all work).
AD_VIDEO = "ad.mp4"

# AD_SOUND = True  -> the ad plays WITH sound.
#   Browsers only allow sound after the visitor has clicked or tapped something,
#   so the popup opens by itself after the visitor's first click or tap
#   (or right away when they press "Watch our ad").
# AD_SOUND = False -> the ad starts muted and the popup opens by itself after 6 seconds.
AD_SOUND = True

ad_state = {"clicked": False, "shown": False}


def render_ad():
    box = q("#ad-media")
    src = AD_VIDEO.strip()

    if AD_SOUND:
        muted_attr = ""
        yt_mute = "0"
    else:
        muted_attr = " muted"
        yt_mute = "1"

    if src == "":
        box.innerHTML = q("#ad-template").innerHTML

    elif src.endswith(".mp4") or src.endswith(".webm"):
        box.innerHTML = (
            '<video controls autoplay' + muted_attr + ' loop playsinline src="' + src + '"></video>'
        )
    else:
        # Convert the YouTube URL into an embed URL
        if "youtu.be/" in src:
            video_id = src.split("youtu.be/")[1].split("?")[0]
            src = "https://www.youtube.com/embed/" + video_id

        elif "/watch?v=" in src:
            video_id = src.split("watch?v=")[1].split("&")[0]
            src = "https://www.youtube.com/embed/" + video_id

        elif "/shorts/" in src:
            video_id = src.split("/shorts/")[1].split("?")[0]
            src = "https://www.youtube.com/embed/" + video_id

        elif "/embed/" in src:
            src = src.split("?")[0]

        # Configure the embedded YouTube player (autoplay and repeat)
        separator = "&" if "?" in src else "?"
        src += separator + "autoplay=1&mute=" + yt_mute + "&rel=0"
        if "/embed/" in src:
            video_id = src.split("/embed/")[1].split("?")[0]
            src += "&loop=1&playlist=" + video_id

        box.innerHTML = (
            '<iframe '
            'src="' + src + '" '
            'title="Ice Cream Cake advertisement" '
            'referrerpolicy="strict-origin-when-cross-origin" '
            'allow="autoplay; encrypted-media; picture-in-picture; web-share" '
            'allowfullscreen></iframe>'
        )


def open_ad(event=None):
    dialog = q("#ad")
    if not dialog.open:
        ad_state["shown"] = True
        render_ad()
        dialog.showModal()


def close_ad(event=None):
    dialog = q("#ad")
    if dialog.open:
        dialog.close()


def clear_ad(event=None):
    q("#ad-media").innerHTML = ""


def mark_click(event=None):
    ad_state["clicked"] = True


async def auto_open_ad():
    await asyncio.sleep(6)
    if AD_SOUND:
        # Wait for the visitor's first click or tap so the browser allows sound
        while not ad_state["clicked"]:
            await asyncio.sleep(0.5)
        await asyncio.sleep(1.5)
    if not ad_state["shown"]:
        open_ad()


# ---- Build the page ----
render_menu()
render_options()
render_bars()

# ---- Connect events ----
for key in FLAVOR_ORDER:
    when("click", "#btn-" + key)(make_flavor_handler(key))

for key in SIZE_ORDER:
    when("click", "#pick-" + key)(make_size_handler(key))

for field_id in ["mode", "cust", "when", "note"]:
    when("input", "#" + field_id)(refresh)
    when("change", "#" + field_id)(refresh)

when("click", "#add-cake")(add_cake)
when("click", "#select-msg")(select_message)

when("click", "body")(mark_click)
when("click", "#watch-ad")(open_ad)
when("click", "#ad-close")(close_ad)
when("click", "#ad-order")(close_ad)
when("close", "#ad")(clear_ad)

# ---- First draw ----
set_flavor("chocolate")
update()

# ---- Pop-up ad opens by itself a few seconds after the page loads ----
try:
    import asyncio
    asyncio.create_task(auto_open_ad())
except ImportError:
    pass
