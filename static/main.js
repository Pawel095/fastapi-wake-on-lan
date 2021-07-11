let TARGETS = undefined

function createRemoveButton(target) {
    let button = $("<button>")
    button.text("Usuń")
    button.on("click", (e) => {
        TARGETS.remove(target.mac)
    })
    return button
}

function createWakeButton(target) {
    let button = $("<button>")
    button.text("Uruchom")
    button.on("click", (e) => {
        $.ajax({
            url: "/send-wol",
            type: "post",
            dataType: "json",
            contentType: 'application/json',
            data: JSON.stringify(target)
        })
    })
    return button
}

class AvailableTargets {
    ORDER = ["name", "description", "ip", "mac", "broadcast"]
    data = []
    constructor() {
        $.ajax({
            url: "/target",
            type: "get",
            success: (response) => {
                this.data = response;
                this.refresh();
            }
        })
    }

    refresh() {
        let tbody = $("<tbody>")
        for (let i = 0; i < this.data.length; i++) {
            const row = this.data[i];
            let tr = $("<tr>")
            this.ORDER.forEach(itemName => {
                let kid = $("<td>");
                kid.text(row[itemName]);
                tr.append(kid)
            });
            tr.append($("<td>").append(createWakeButton(row)));
            tr.append($("<td>").append(createRemoveButton(row)));
            tbody.append(tr)
        }
        $("table#targets>tbody").replaceWith(tbody)
    }

    add(target) {
        $.ajax({
            url: "/target",
            type: "post",
            dataType: "json",
            contentType: 'application/json',
            data: JSON.stringify(target),
            success: (response) => {
                this.data.push(response)
                this.refresh()
            },
        });
    }
    remove(mac) {
        $.ajax({
            url: `/target?mac=${mac}`,
            type: "delete",
            data: JSON.stringify({ "mac": mac }),
            success: (response) => {
                this.data = this.data.filter((e) => e.mac != mac)
                this.refresh()
            },
        });
    }
}


$(window).on("load", init)

function form2json() {
    ret = Object()
    for (const i of $("*[data-dbname]")) {
        ret[i.dataset.dbname] = i.value
    }
    return ret
}

function init() {
    TARGETS = new AvailableTargets()
    $("form#addNew").on("submit", (e) => {
        e.preventDefault()
        TARGETS.add(form2json())
    })
}
