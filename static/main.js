const DEFAULT_STATUS_TEXT = "Nieznany"
const SEND_WOL_TEXT = "Uruchom"
const DELETE_TARGET_TEXT = "Usuń"
const START_PINGING_TEXT = "Rozpocznij Sprawdzanie"
const STOP_PINGING_TEXT = "Zakończ Sprawdzanie"

let TARGETS = undefined

function createRemoveButton(target) {
    let button = $("<button>")
    button.text(DELETE_TARGET_TEXT)
    button.on("click", (e) => {
        TARGETS.remove(target.mac)
    })
    return button
}

function createWakeButton(target) {
    let button = $("<button>")
    button.text(SEND_WOL_TEXT)
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
function createStatusToggle(target, outputElement) {
    let button = $("<button>")
    let ws = undefined
    function StartPinging(e) {
        button.text(STOP_PINGING_TEXT)
        button.on("click", StopPinging)

        ws = new WebSocket(`ws://${window.location.host}/ws`)
        ws.addEventListener("open", e => {
            ws.send(target.ip)
            ws.send("requesting")
        })
        ws.addEventListener("message", (e) => {
            data = JSON.parse(e.data)
            outputElement.text(data.text)
            console.log(data, data.code === 0)
            if (data.code === 0) {
                outputElement.css("background", "LightCoral")
            } else {
                outputElement.css("background", "lightgreen")
            }
            setTimeout(() => {
                outputElement.css("background", "transparent")
            }, 1500);
            setTimeout(() => {
                ws.send("requesting")
            }, 3000);
        })
    }
    function StopPinging(e) {
        button.text(START_PINGING_TEXT)
        button.on("click", StartPinging)

        ws.close()
    }
    button.text(START_PINGING_TEXT)
    button.on("click", StartPinging)
    return button
}
function form2json() {
    ret = Object()
    for (const i of $("*[data-dbname]")) {
        ret[i.dataset.dbname] = i.value
    }
    return ret
}
class Tables {
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
    refreshTargets() {
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
    refreshStatus() {
        let tbody = $("<tbody>")
        for (let i = 0; i < this.data.length; i++) {
            const row = this.data[i];
            let tr = $("<tr>")
            tr.append($("<td>").text(row.name))
            let outCell = $("<td>").text(DEFAULT_STATUS_TEXT)
            outCell.toggleClass("Transition-1s")
            tr.append(outCell)
            tr.append($("<td>").append(createStatusToggle(row, outCell)))
            tbody.append(tr)
        }
        $("table#status>tbody").replaceWith(tbody)
    }

    refresh() {
        this.refreshTargets()
        this.refreshStatus()
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

function init() {
    TARGETS = new Tables()
    $("form#addNew").on("submit", (e) => {
        e.preventDefault()
        TARGETS.add(form2json())
    })
}
