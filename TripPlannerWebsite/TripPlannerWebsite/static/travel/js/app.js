const qs = (selector, root = document) => root.querySelector(selector);
const qsa = (selector, root = document) => [...root.querySelectorAll(selector)];

function readJsonScript(id, fallback) {
    const node = document.getElementById(id);
    if (!node) return fallback;
    try {
        return JSON.parse(node.textContent);
    } catch {
        return fallback;
    }
}

function setupMobileMenu() {
    const toggle = qs("[data-menu-toggle]");
    const menu = qs("[data-site-menu]");
    if (!toggle || !menu) return;

    toggle.addEventListener("click", () => {
        const isOpen = menu.classList.toggle("is-open");
        toggle.setAttribute("aria-expanded", String(isOpen));
        document.body.classList.toggle("menu-open", isOpen);
    });

    qsa("a", menu).forEach((link) => {
        link.addEventListener("click", () => {
            menu.classList.remove("is-open");
            document.body.classList.remove("menu-open");
            toggle.setAttribute("aria-expanded", "false");
        });
    });
}

function setupScrollTools() {
    const progress = qs("[data-scroll-progress]");
    const backToTop = qs("[data-back-to-top]");

    const update = () => {
        const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
        const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const percent = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
        if (progress) progress.style.width = `${percent}%`;
        if (backToTop) backToTop.classList.toggle("is-visible", scrollTop > 420);
    };

    window.addEventListener("scroll", update, { passive: true });
    update();

    if (backToTop) {
        backToTop.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
    }
}

function setupCounters() {
    qsa("[data-count-to]").forEach((counter) => {
        const target = Number(counter.dataset.countTo || "0");
        let current = 0;
        const step = Math.max(1, Math.ceil(target / 30));
        const tick = () => {
            current = Math.min(target, current + step);
            counter.textContent = current;
            if (current < target) requestAnimationFrame(tick);
        };
        tick();
    });
}

function filterCards() {
    const searchInput = qs("[data-card-search]");
    const sortSelect = qs("[data-card-sort]");
    const grids = qsa("[data-filter-grid]");
    if (!grids.length) return;

    const apply = () => {
        const term = (searchInput?.value || "").trim().toLowerCase();
        const sort = sortSelect?.value || "default";

        grids.forEach((grid) => {
            const cards = qsa("[data-search-text]", grid);
            cards.forEach((card) => {
                const haystack = (card.dataset.searchText || "").toLowerCase();
                card.hidden = term.length > 0 && !haystack.includes(term);
            });

            if (sort !== "default") {
                cards
                    .sort((a, b) => {
                        if (sort === "name") return (a.dataset.name || "").localeCompare(b.dataset.name || "");
                        return Number(a.dataset.price || "0") - Number(b.dataset.price || "0");
                    })
                    .forEach((card) => grid.appendChild(card));
            }
        });
    };

    searchInput?.addEventListener("input", apply);
    sortSelect?.addEventListener("change", apply);
    apply();
}

function setupTransportTable() {
    const searchInput = qs("[data-table-search]");
    const methodFilter = qs("[data-transport-filter]");
    const rows = qsa("[data-row-text]");
    if (!rows.length) return;

    const apply = () => {
        const term = (searchInput?.value || "").trim().toLowerCase();
        const method = methodFilter?.value || "";
        rows.forEach((row) => {
            const textMatches = (row.dataset.rowText || "").toLowerCase().includes(term);
            const methodMatches = !method || row.dataset.method === method;
            row.hidden = !textMatches || !methodMatches;
        });
    };

    searchInput?.addEventListener("input", apply);
    methodFilter?.addEventListener("change", apply);
    apply();
}

function setupChecklist() {
    const checklist = qs("[data-trip-checklist]");
    const progress = qs("[data-checklist-progress]", checklist || document);
    if (!checklist || !progress) return;

    const boxes = qsa("input[type='checkbox']", checklist);
    const update = () => {
        progress.value = boxes.filter((box) => box.checked).length;
    };
    boxes.forEach((box) => box.addEventListener("change", update));
    update();
}

function setupBookingForm() {
    const form = qs("[data-booking-form]");
    if (!form) return;

    const bookingType = qs("#id_booking_type", form);
    const destination = qs("#id_destination", form);
    const hotelLabel = qs("#id_hotel", form)?.closest("label");
    const transportLabel = qs("#id_transport", form)?.closest("label");
    const packageLabel = qs("#id_holiday_package", form)?.closest("label");
    const checkInLabel = qs("#id_check_in_date", form)?.closest("label");
    const checkOutLabel = qs("#id_check_out_date", form)?.closest("label");
    const travelDateLabel = qs("#id_travel_date", form)?.closest("label");
    const travelers = qs("#id_travelers", form);
    const summary = qs("[data-booking-summary]");

    const setRequired = (label, enabled) => {
        if (!label) return;
        label.classList.toggle("is-muted", !enabled);
        const field = qs("input, select, textarea", label);
        if (field && !enabled) field.value = "";
    };

    const update = () => {
        const type = bookingType?.value || "hotel";
        setRequired(hotelLabel, type === "hotel");
        setRequired(transportLabel, type === "transport");
        setRequired(packageLabel, type === "package");
        setRequired(checkInLabel, type === "hotel" || type === "package");
        setRequired(checkOutLabel, type === "hotel" || type === "package");
        setRequired(travelDateLabel, type === "transport" || type === "package");

        const typeName = bookingType?.selectedOptions?.[0]?.text || "booking";
        const destinationName = destination?.selectedOptions?.[0]?.text || "your destination";
        const people = travelers?.value || "1";
        if (summary) {
            summary.textContent = `${typeName} request for ${destinationName}, planned for ${people} traveler(s).`;
        }
    };

    [bookingType, destination, travelers].forEach((field) => field?.addEventListener("change", update));
    travelers?.addEventListener("input", update);
    update();
}

function setupRouteSearch() {
    const form = qs("[data-route-search]");
    if (!form) return;

    const root = form.dataset.searchRoot || "/search/";
    const fromInput = qs("input[name='from']", form);
    const toInput = qs("input[name='to']", form);
    const swap = qs("[data-swap-route]", form);
    const tabs = qsa("[data-service-tab]");
    const promoPanels = qsa("[data-promo-panel]");
    const routeOnlyRows = qsa("[data-route-only]", form);
    const routeFields = qs("[data-route-fields]", form);
    const stayFields = qs("[data-stay-fields]", form);
    const destinationFields = qs("[data-destination-fields]", form);
    const serviceModes = readJsonScript("service-modes-data", {});

    const setDisabled = (rootNode, disabled) => {
        if (!rootNode) return;
        rootNode.hidden = disabled;
        qsa("input, select, button", rootNode).forEach((field) => {
            if (!field.matches("[data-service-tab]")) field.disabled = disabled;
        });
    };

    const applyMode = (service) => {
        const mode = serviceModes[service] || "route";
        setDisabled(routeFields, mode !== "route");
        setDisabled(stayFields, mode !== "stay");
        setDisabled(destinationFields, mode !== "destination");
        routeOnlyRows.forEach((row) => {
            row.hidden = mode !== "route";
            qsa("input, select", row).forEach((field) => {
                field.disabled = mode !== "route";
            });
        });
    };

    tabs.forEach((tab) => {
        tab.addEventListener("click", () => {
            tabs.forEach((item) => item.classList.remove("is-active"));
            tab.classList.add("is-active");
            form.action = `${root}${tab.dataset.serviceTab}/`;
            applyMode(tab.dataset.serviceTab);
            promoPanels.forEach((panel) => {
                panel.classList.toggle("is-active", panel.dataset.promoPanel === tab.dataset.serviceTab);
            });
        });
    });

    swap?.addEventListener("click", () => {
        if (!fromInput || !toInput) return;
        const nextFrom = toInput.value;
        toInput.value = fromInput.value;
        fromInput.value = nextFrom;
    });

    const active = qs("[data-service-tab].is-active");
    applyMode(active?.dataset.serviceTab || "flights");
}

function setupDateDisplays() {
    qsa("[data-date-input]").forEach((input) => {
        const label = input.closest("label");
        const display = qs("[data-date-display]", label || document);
        if (!display) return;

        const update = () => {
            if (!input.value) {
                if (input.name === "return") display.textContent = "Save more together";
                else if (input.name === "checkout") display.textContent = "Select date";
                else display.textContent = "Choose date";
                return;
            }
            const selected = new Date(`${input.value}T00:00:00`);
            display.textContent = selected.toLocaleDateString("en-IN", {
                weekday: "short",
                day: "numeric",
                month: "short",
                year: "numeric",
            });
        };

        label?.addEventListener("click", () => {
            if (typeof input.showPicker === "function") input.showPicker();
        });
        input.addEventListener("change", update);
        update();
    });
}

function setupAutocomplete() {
    const routeSuggestions = readJsonScript("route-suggestions-data", []);
    const staySuggestions = readJsonScript("stay-suggestions-data", []);
    let activeBox = null;

    const closeBox = () => {
        activeBox?.remove();
        activeBox = null;
    };

    const render = (input) => {
        closeBox();
        const source = input.dataset.suggestType === "stay" ? staySuggestions : routeSuggestions;
        const term = input.value.trim().toLowerCase();
        const matches = source
            .filter((item) => !term || item.toLowerCase().includes(term))
            .slice(0, 8);
        if (!matches.length) return;

        const box = document.createElement("div");
        box.className = "suggestion-box";
        box.innerHTML = `
            <div class="suggestion-search">Search: "${input.value || "popular places"}"</div>
            ${matches.map((item) => `<button type="button">${item}</button>`).join("")}
        `;
        input.closest(".suggest-field")?.appendChild(box);
        activeBox = box;

        qsa("button", box).forEach((button) => {
            button.addEventListener("click", () => {
                input.value = button.textContent;
                closeBox();
            });
        });
    };

    qsa("[data-suggest-input]").forEach((input) => {
        input.addEventListener("input", () => render(input));
        input.addEventListener("focus", () => render(input));
    });

    document.addEventListener("click", (event) => {
        if (!event.target.closest(".suggest-field")) closeBox();
    });
}

function highlightPrices() {
    const prices = qsa("[data-price-value]");
    if (!prices.length) return;
    const values = prices.map((item) => Number(item.dataset.priceValue || "0")).filter(Boolean);
    const lowest = Math.min(...values);
    prices.forEach((item) => {
        if (Number(item.dataset.priceValue || "0") === lowest) {
            item.insertAdjacentHTML("beforeend", " <span class=\"deal-badge\">Best value</span>");
        }
    });
}

function setupSavedTrips() {
    const buttons = qsa("[data-save-trip]");
    const savedCount = qs("[data-saved-count]");
    const userKey = document.body.dataset.userKey || "guest";
    const storageKey = `travelmate.savedTrips.${userKey}`;
    const getSaved = () => JSON.parse(localStorage.getItem(storageKey) || "[]");
    const setSaved = (items) => {
        localStorage.setItem(storageKey, JSON.stringify(items));
        if (savedCount) savedCount.textContent = `Saved trips: ${items.length}`;
        buttons.forEach((button) => {
            const isSaved = items.includes(button.dataset.saveTrip);
            button.classList.toggle("is-saved", isSaved);
            button.textContent = isSaved ? "Saved" : "Save";
        });
    };

    buttons.forEach((button) => {
        button.addEventListener("click", () => {
            const name = button.dataset.saveTrip;
            const saved = getSaved();
            const next = saved.includes(name) ? saved.filter((item) => item !== name) : [...saved, name];
            setSaved(next);
        });
    });

    setSaved(getSaved());
}

document.addEventListener("DOMContentLoaded", () => {
    setupMobileMenu();
    setupScrollTools();
    setupCounters();
    filterCards();
    setupTransportTable();
    setupChecklist();
    setupBookingForm();
    setupRouteSearch();
    setupDateDisplays();
    setupAutocomplete();
    highlightPrices();
    setupSavedTrips();
});
