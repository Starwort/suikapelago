// const Matter = require('matter-js');

function mulberry32(a) {
    return function () {
        let t = a += 0x6D2B79F5;
        t = Math.imul(t ^ t >>> 15, t | 1);
        t ^= t + Math.imul(t ^ t >>> 7, t | 61);
        return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
}

const rand = mulberry32(Date.now());

const {
    Engine, Render, Runner, Composites, Common, MouseConstraint, Mouse,
    Composite, Bodies, Events,
} = Matter;

const wallPad = 64;
const maxLoseHeight = 84;
const playAreaBottom = 912;
const statusBarHeight = 48;
const previewBallHeight = 32;
const friction = {
    friction: 0.006,
    frictionStatic: 0.006,
    frictionAir: 0,
    restitution: 0.1
};

const GameStates = {
    MENU: 0,
    READY: 1,
    DROP: 2,
    LOSE: 3,
};

const Game = {
    width: 640,
    height: 960,
    _loseHeight: maxLoseHeight,
    get loseHeight() {
        return this._loseHeight;
    },
    set loseHeight(value) {
        this._loseHeight = value;
        this.elements.gameCeiling.style.setProperty("--lose-height", value);
    },
    elements: {
        canvas: document.getElementById('game-canvas'),
        ui: document.getElementById('game-ui'),
        score: document.getElementById('game-score'),
        end: document.getElementById('game-end-container'),
        endTitle: document.getElementById('game-end-title'),
        next: document.getElementById("next"),
        nextFruitImg: document.getElementById('game-next-fruit'),
        scoresanityNext: document.getElementById('next-check'),
        scoresanityLabel: document.getElementById('scoresanity-label'),
        gameCeiling: document.getElementById("game-ceiling"),
        previewBall: null,
    },
    sounds: {
        click: new Audio('./assets/click.mp3'),
        pop0: new Audio('./assets/pop0.mp3'),
        pop1: new Audio('./assets/pop1.mp3'),
        pop2: new Audio('./assets/pop2.mp3'),
        pop3: new Audio('./assets/pop3.mp3'),
        pop4: new Audio('./assets/pop4.mp3'),
        pop5: new Audio('./assets/pop5.mp3'),
        pop6: new Audio('./assets/pop6.mp3'),
        pop7: new Audio('./assets/pop7.mp3'),
        pop8: new Audio('./assets/pop8.mp3'),
        pop9: new Audio('./assets/pop9.mp3'),
        pop10: new Audio('./assets/pop10.mp3'),
        notify: new Audio('./assets/notify.mp3'),
    },

    stateIndex: GameStates.MENU,

    score: 0,
    fruitsMerged: [],
    bonusPoints: 0,
    _scoreThresholds: null,
    get scoreThresholds() {
        if (this._scoreThresholds) {
            return this._scoreThresholds;
        } else {
            return this._scoreThresholds = Array.from(
                {length: 20},
                (_, threshold) => Math.ceil((1500 + 500 * Game.scoresanityDifficulty) * Math.pow((threshold + 1) / 20, 2.5))
            );
        }
    },
    calculateScore: function () {
        const score = Game.fruitsMerged.reduce((total, count, sizeIndex) => {
            const value = Game.fruitSizes[sizeIndex].scoreValue * count;
            return total + value;
        }, 0);

        let newScore = score + Game.bonusPoints * Game.bonusPoints * 5;
        if (Game.scoresanity) {
            for (let i = 0; i < 20; i++) {
                const scoreThreshold = Game.scoreThresholds[i];
                if (Game.score < scoreThreshold && scoreThreshold <= newScore) {
                    apClient.check(i + 11);
                    if (i == 19) {
                        Game.elements.scoresanityNext.innerText = "N/A";
                    } else {
                        Game.elements.scoresanityNext.innerText = Game.scoreThresholds[i + 1];
                    }
                }
            }
            if (newScore >= this.scoreThresholds[19] && (
                this.goal == 1 || (this.goal == 2 && this.bestSize == 10)
            )) {
                apClient.goal();
            }
        }
        Game.elements.score.innerText = Game.score = newScore;
    },

    fruitSizes: [
        {radius: 24, scoreValue: 1, img: './assets/img/circle0.png'},
        {radius: 32, scoreValue: 3, img: './assets/img/circle1.png'},
        {radius: 40, scoreValue: 6, img: './assets/img/circle2.png'},
        {radius: 56, scoreValue: 10, img: './assets/img/circle3.png'},
        {radius: 64, scoreValue: 15, img: './assets/img/circle4.png'},
        {radius: 72, scoreValue: 21, img: './assets/img/circle5.png'},
        {radius: 84, scoreValue: 28, img: './assets/img/circle6.png'},
        {radius: 96, scoreValue: 36, img: './assets/img/circle7.png'},
        {radius: 128, scoreValue: 45, img: './assets/img/circle8.png'},
        {radius: 160, scoreValue: 55, img: './assets/img/circle9.png'},
        {radius: 192, scoreValue: 66, img: './assets/img/circle10.png'},
    ],
    currentFruitSize: 0,
    nextFruitSize: 0,
    _maxFruitSize: 2,

    set hasNext(value) {
        if (value) {
            Game.elements.next.style.removeProperty("display");
        } else {
            Game.elements.next.style.display = "none";
        }
    },

    get maxFruitSize() {
        return this._maxFruitSize;
    },
    set maxFruitSize(value) {
        for (let i = 0; i < 11; i++) {
            if (i <= value) {
                this.fruitSizes[i].imgEl.classList.remove("circle-unavailable");
            } else {
                this.fruitSizes[i].imgEl.classList.add("circle-unavailable");
            }
        }
        this._maxFruitSize = value;
    },
    setNextFruitSize: function () {
        Game.nextFruitSize = Math.min(Math.floor(Math.pow(rand(), 2) * 5), Game.maxFruitSize);
        Game.elements.nextFruitImg.src = Game.fruitSizes[Game.nextFruitSize].img;
    },

    initGame: function () {
        Render.run(render);
        Runner.run(runner, engine);

        Composite.add(engine.world, menuStatics);

        Game.fruitsMerged = Array.apply(null, Array(Game.fruitSizes.length)).map(() => 0);
    },

    startGame: function () {
        Game.sounds.click.play();

        Composite.remove(engine.world, menuStatics);
        Composite.add(engine.world, gameStatics);

        Game.calculateScore();
        Game.elements.endTitle.innerText = 'Game Over!';
        Game.elements.ui.style.display = 'block';
        Game.elements.end.style.display = 'none';
        Game.elements.previewBall = Game.generateFruitBody(Game.width / 2, previewBallHeight, 0, {isStatic: true});
        Composite.add(engine.world, Game.elements.previewBall);

        setTimeout(() => {
            Game.stateIndex = GameStates.READY;
        }, 250);

        Events.on(mouseConstraint, 'mouseup', function (e) {
            Game.addFruit(e.mouse.position.x);
        });

        Events.on(mouseConstraint, 'mousemove', function (e) {
            if (Game.stateIndex !== GameStates.READY) return;
            if (Game.elements.previewBall === null) return;

            Game.elements.previewBall.position.x = e.mouse.position.x;
        });

        Events.on(engine, 'collisionStart', function (e) {
            for (let i = 0; i < e.pairs.length; i++) {
                const {bodyA, bodyB} = e.pairs[i];

                // Skip if collision is wall
                if (bodyA.isStatic || bodyB.isStatic) continue;

                const aY = bodyA.position.y + bodyA.circleRadius;
                const bY = bodyB.position.y + bodyB.circleRadius;

                // Uh oh, too high!
                if (aY < Game.loseHeight || bY < Game.loseHeight) {
                    if (this.deathLink) {
                        apClient.deathLink.sendDeathLink(apClient.name, `${apClient.name} topped out!`);
                    }
                    Game.loseGame();
                    return;
                }

                // Skip different sizes
                if (bodyA.sizeIndex !== bodyB.sizeIndex) continue;

                // Skip fruits that are too big
                if (bodyA.sizeIndex >= Game.maxFruitSize) continue;

                // Skip if already popped
                if (bodyA.popped || bodyB.popped) continue;

                let newSize = bodyA.sizeIndex + 1;

                // Go back to smallest size
                if (bodyA.circleRadius >= Game.fruitSizes[Game.fruitSizes.length - 1].radius) {
                    newSize = 0;
                }

                Game.fruitsMerged[bodyA.sizeIndex] += 1;

                // Therefore, circles are same size, so merge them.
                const midPosX = (bodyA.position.x + bodyB.position.x) / 2;
                const midPosY = (bodyA.position.y + bodyB.position.y) / 2;

                bodyA.popped = true;
                bodyB.popped = true;

                Game.sounds[`pop${bodyA.sizeIndex}`].play();
                Composite.remove(engine.world, [bodyA, bodyB]);
                Composite.add(engine.world, Game.generateFruitBody(midPosX, midPosY, newSize));
                Game.addPop(midPosX, midPosY, bodyA.circleRadius);
                Game.calculateScore();
            }
        });
    },

    addPop: function (x, y, r) {
        const circle = Bodies.circle(x, y, r, {
            isStatic: true,
            collisionFilter: {mask: 0x0040},
            angle: rand() * (Math.PI * 2),
            render: {
                sprite: {
                    texture: './assets/img/pop.png',
                    xScale: r / 384,
                    yScale: r / 384,
                }
            },
        });

        Composite.add(engine.world, circle);
        setTimeout(() => {
            Composite.remove(engine.world, circle);
        }, 100);
    },

    loseGame: function () {
        Game.stateIndex = GameStates.LOSE;
        Game.elements.end.style.display = 'flex';
        runner.enabled = false;
        // Game.startGame();

        setTimeout(() => {
            const bodies = engine.world.bodies
                .slice(3) // game walls
                .filter(i => i.id != Game.elements.previewBall.id);
            for (const body of bodies) {
                Matter.Composite.remove(engine.world, body);
            }

            Game.startGame();
            runner.enabled = true;
        }, 1000);
    },

    // Returns an index, or null
    lookupFruitIndex: function (radius) {
        const sizeIndex = Game.fruitSizes.findIndex(size => size.radius == radius);
        if (sizeIndex === undefined) return null;
        if (sizeIndex === Game.fruitSizes.length - 1) return null;

        return sizeIndex;
    },

    bestSize: -1,
    generateFruitBody: function (x, y, sizeIndex, extraConfig = {}) {
        if (sizeIndex > this.bestSize) {
            for (let i = sizeIndex; i > this.bestSize; i--) {
                apClient.check(Game.fruitSizes[i].location);
            }
            if (sizeIndex == 10 && (
                this.goal == 0
                || (this.goal == 2 && this.score >= this.scoreThresholds[19])
            )) {
                apClient.goal();
            }
            this.bestSize = sizeIndex;
        }
        const size = Game.fruitSizes[sizeIndex];
        const circle = Bodies.circle(x, y, size.radius, {
            ...friction,
            ...extraConfig,
            render: {sprite: {texture: size.img, xScale: size.radius / 512, yScale: size.radius / 512}},
        });
        circle.sizeIndex = sizeIndex;
        circle.popped = false;

        return circle;
    },

    cooldown: 0,
    addFruit: function (x) {
        if (Game.stateIndex !== GameStates.READY) return;

        Game.sounds.click.play();

        Game.stateIndex = GameStates.DROP;
        const latestFruit = Game.generateFruitBody(x, previewBallHeight, Game.currentFruitSize);
        Composite.add(engine.world, latestFruit);

        Game.currentFruitSize = Game.nextFruitSize;
        Game.setNextFruitSize();
        Game.calculateScore();

        Composite.remove(engine.world, Game.elements.previewBall);
        Game.elements.previewBall = Game.generateFruitBody(render.mouse.position.x, previewBallHeight, Game.currentFruitSize, {
            isStatic: true,
            collisionFilter: {mask: 0x0040}
        });

        let shouldNotify = Game.cooldown > 5_000;

        setTimeout(() => {
            if (Game.stateIndex === GameStates.DROP) {
                Composite.add(engine.world, Game.elements.previewBall);
                Game.stateIndex = GameStates.READY;
                if (shouldNotify) {
                    Game.sounds.notify.play();
                }
            }
        }, 500 + Game.cooldown);
    }
};

/// PROGRESSION ///
const PROG_HEIGHT = "Progressive Field Height";
const PROG_FRUIT = "Progressive Max Fruit";
const PROG_NEXT = "Next Fruit View";

/// USEFUL ///
const USEF_DROP_COOLDOWN = "Progressive Drop Cooldown Reduction";
const USEF_POINTS = "Progressive Bonus Points";

/// TRAPS ///
// causes the lined-up fruit to be dropped instantly
const TRAP_INSTA_DROP = "Instant Drop Trap";
// the position of each fruit is swapped with another fruit, at random (FY-shuffle?)
const TRAP_SHUFFLE = "Shuffle Trap";
// applies a large impulse to the bottom of the board
const TRAP_IMPULSE = "Impulse Trap";
// deletes 50% of fruits on the board, at random
const TRAP_THANOS = "Thanos Trap";

const apClient = new Client();

const windowLogin = (/** @type{HTMLButtonElement} */document.getElementById("login"));
const windowChat = (/** @type{HTMLButtonElement} */document.getElementById("chat"));

const loginButton = (/** @type{HTMLButtonElement} */document.getElementById("connect"));
const loginStatus = (/** @type{HTMLDivElement} */document.getElementById("connect-error"));
const serverInput = (/** @type{HTMLInputElement} */document.getElementById("server"));
const slotInput = (/** @type{HTMLInputElement} */document.getElementById("slot"));
const passwordInput = (/** @type{HTMLInputElement} */document.getElementById("password"));

const chatLog = (/** @type{HTMLDivElement} */document.getElementById("chat-log"));
const chatBox = (/** @type{HTMLInputElement} */document.getElementById("chat-box"));
const chatSend = (/** @type{HTMLButtonElement} */document.getElementById("chat-send"));

const writeChatMsg = (
    _plainText,
    /** @type{(
        ItemMessageNode
        | LocationMessageNode
        | ColorMessageNode
        | TextualMessageNode
        | PlayerMessageNode
    )[]} */ nodes
) => {
    const newMessage = document.createElement("span");
    for (const node of nodes) {
        const messagePart = document.createElement("span");
        messagePart.innerText = node.text;
        switch (node.type) {
            case "item":
                const item = node.item;
                if (item.progression) {
                    messagePart.classList.add("progression");
                }
                if (item.useful) {
                    messagePart.classList.add("useful");
                }
                if (item.trap) {
                    messagePart.classList.add("trap");
                }
                if (item.filler) {
                    messagePart.classList.add("filler");
                }
                break;
            case "location":
                messagePart.classList.add("location");
                break;
            case "color":
                messagePart.classList.add(node.color);
                break;
            case "text":
            case "entrance":
                break;
            case "player":
                messagePart.classList.add(
                    node.player.name == apClient.name
                        ? "local-player"
                        : "other-player"
                );
                break;
            default:
                console.log("Error parsing node type " + node.type);
        }
        newMessage.appendChild(messagePart);
    }
    chatLog.appendChild(newMessage);
};

apClient.messages.on("message",
    writeChatMsg,
);

let nextIdx = 0;
const getItems = (items, index) => {
    if (items && items.length) {
        if (index > nextIdx) {
            console.log("Expected index:", nextIdx, "but got:", index, items);
        }
        nextIdx = index + 1;
        for (const item of items) {
            switch (item.name) {
                case PROG_FRUIT:
                    Game.sounds.notify.play();
                    Game.maxFruitSize++;
                    break;
                case PROG_HEIGHT:
                    Game.heightUpgrades++;
                    const heightUpgradeProgress = (0.5 - Game.heightUpgrades / (2 * Game.maxHeightUpgrades));
                    Game.loseHeight = heightUpgradeProgress * (playAreaBottom - maxLoseHeight) + maxLoseHeight;
                    break;
                case PROG_NEXT:
                    Game.hasNext = true;
                    break;
                case USEF_DROP_COOLDOWN:
                    Game.cooldownReductions++;
                    Game.cooldown = 60_000 * (1 - Game.cooldownReductions / Game.maxCooldownReductions);
                    break;
                case USEF_POINTS:
                    Game.bonusPoints++;
                    Game.calculateScore();
                    break;
                case TRAP_IMPULSE:
                    trapImpulse();
                    break;
                case TRAP_SHUFFLE:
                    trapShuffle();
                    break;
                case TRAP_THANOS:
                    trapThanos();
                    break;
                case TRAP_INSTA_DROP:
                    Game.addFruit(Game.elements.previewBall.position.x);
                    break;
            }
        }
    }
};

function trapImpulse() {
    // Check each fruit for collision with the floor, then apply
    // a large impulse
    for (let i = 3; i < engine.world.bodies.length; i++) {
        if (Matter.Collision.collides(engine.world.bodies[2], engine.world.bodies[i])) {
            engine.world.bodies[i].constraintImpulse.y = -15;
        }
    }
}

function trapShuffle() {
    // Collect each body's position, then shuffle them
    const bodies = engine.world.bodies
        .slice(3) // game walls
        .filter(i => i.id != Game.elements.previewBall.id);
    const bodyPositions = bodies.map(body => ({...body.position}));
    shuffle(bodyPositions);
    for (let i = 0; i < bodyPositions.length; i++) {
        Matter.Body.setPosition(bodies[i], bodyPositions[i], false);
    }
}

function trapThanos() {
    // Collect each body, shuffle them, then delete the latter half
    const bodies = engine.world.bodies
        .slice(3) // game walls
        .filter(i => i.id != Game.elements.previewBall.id);
    shuffle(bodies);
    for (const body of bodies.slice(Math.floor(bodies.length / 2))) {
        Matter.Composite.remove(engine.world, body);
    }
}

apClient.items.on("itemsReceived", (...args) => setTimeout(getItems, 0, ...args));

function shuffle(array) {
    for (let i = array.length; --i > 0;) {
        const j = Math.floor(rand() * (i + 1));
        [array[j], array[i]] = [array[i], array[j]];
    }
}

apClient.deathLink.on("deathReceived", (source, time, cause) => {
    if (cause) {
        writeChatMsg(null, [{type: "color", text: cause, color: "red"}]);
    } else {
        writeChatMsg(null, [{type: "player", text: source, player: {name: source}}, {type: "color", text: " died", color: "red"}]);
    }
    if (Game.deathLink) {
        Game.loseGame();
    }
});

loginButton?.addEventListener("click", async () => {
    loginStatus.innerText = "Attempting to log in...";
    loginStatus.classList.remove("error");
    try {
        const {
            deathlink,
            shuffle_fruit,
            height_upgrade_count,
            cooldown_upgrade_count,
            goal,
            scoresanity,
            difficulty,
            max_fruit_size,
            next_needs_unlock,
        } = await apClient.login(serverInput.value, slotInput.value, "Suikapelago", {
            password: passwordInput.value,
            tags: ["DeathLink"],
        });
        console.log({
            deathlink,
            shuffle_fruit,
            height_upgrade_count,
            cooldown_upgrade_count,
            goal,
            scoresanity,
            difficulty,
            max_fruit_size,
            next_needs_unlock,
        });
        const FRUIT_NAMES = [
            "Cherry",
            "Strawberry",
            "Grapes",
            "Dekopon",
            "Persimmon",
            "Apple",
            "Pear",
            "Peach",
            "Pineapple",
            "Melon",
            "Watermelon",
        ];
        for (let i = 0; i < 11; i++) {
            Game.fruitSizes[i].name = FRUIT_NAMES[i];
            Game.fruitSizes[i].imgEl = document.querySelector(`#circle-${i}`);
            Game.fruitSizes[i].location = i;
            if (i > 0) {
                Game.fruitSizes[i].imgEl.classList.add("circle-unavailable");
            }
        }
        if (shuffle_fruit) {
            document.querySelector("#circle").classList.add("shuffled");
            for (let i = 0; i < 11; i++) {
                const targetFruit = shuffle_fruit[i];
                Game.fruitSizes[i].imgEl.src =
                    Game.fruitSizes[i].img = `./assets/img/circle${targetFruit}.png`;
                Game.fruitSizes[i].name = FRUIT_NAMES[targetFruit];
                Game.fruitSizes[i].location = targetFruit;
            }
        }
        if (height_upgrade_count != 0) {
            Game.loseHeight = maxLoseHeight + (playAreaBottom - maxLoseHeight) / 2;
            Game.heightUpgrades = 0;
            Game.maxHeightUpgrades = height_upgrade_count;
        }
        if (cooldown_upgrade_count != 0) {
            Game.cooldownReductions = 0;
            Game.maxCooldownReductions = cooldown_upgrade_count;
            Game.cooldown = 60_000;
        }
        Game.hasNext = !next_needs_unlock;
        Game.goal = goal;
        Game.scoresanity = scoresanity;
        Game.scoresanityDifficulty = difficulty;
        Game.maxFruitSize = max_fruit_size - 1;
        Game.deathLink = deathlink;
        if (scoresanity) {
            Game.elements.scoresanityNext.innerText = Game.scoreThresholds[0];
        } else {
            Game.elements.scoresanityLabel.display = "none";
            Game.elements.scoresanityNext.display = "none";
        }
        Game.startGame();
        windowLogin.style.display = "none";
        windowChat.style.removeProperty("display");
    } catch (e) {
        loginStatus.innerText = e.toString();
        loginStatus.classList.add("error");
    }
});

const engine = Engine.create();
const runner = Runner.create();
const render = Render.create({
    element: Game.elements.canvas,
    engine,
    options: {
        width: Game.width,
        height: Game.height,
        wireframes: false,
        background: '#ffdcae'
    }
});

const menuStatics = [
    Bodies.rectangle(Game.width / 2, Game.height * 0.4, 512, 512, {
        isStatic: true,
        render: {sprite: {texture: './assets/img/bg-menu.png'}},
    }),

    // Add each fruit in a circle
    ...Array.apply(null, Array(Game.fruitSizes.length)).map((_, index) => {
        const x = (Game.width / 2) + 192 * Math.cos((Math.PI * 2 * index) / 12);
        const y = (Game.height * 0.4) + 192 * Math.sin((Math.PI * 2 * index) / 12);
        const r = 64;

        return Bodies.circle(x, y, r, {
            isStatic: true,
            render: {
                sprite: {
                    texture: Game.fruitSizes[index].img,
                    xScale: r / 1024,
                    yScale: r / 1024,
                },
            },
        });
    }),
];

const wallProps = {
    isStatic: true,
    render: {fillStyle: '#FFEEDB'},
    ...friction,
};

const gameStatics = [
    // Left
    Bodies.rectangle(-(wallPad / 2), Game.height / 2, wallPad, Game.height, wallProps),

    // Right
    Bodies.rectangle(Game.width + (wallPad / 2), Game.height / 2, wallPad, Game.height, wallProps),

    // Bottom
    Bodies.rectangle(Game.width / 2, Game.height + (wallPad / 2) - statusBarHeight, Game.width, wallPad, wallProps),
];

// add mouse control
const mouse = Mouse.create(render.canvas);
const mouseConstraint = MouseConstraint.create(engine, {
    mouse: mouse,
    constraint: {
        stiffness: 0.2,
        render: {
            visible: false,
        },
    },
});
render.mouse = mouse;

Game.initGame();

const resizeCanvas = () => {
    const screenWidth = document.body.clientWidth;
    const screenHeight = document.body.clientHeight;

    let newWidth = Game.width;
    let newHeight = Game.height;
    let scaleUI = 1;

    if (screenWidth * 1.5 > screenHeight) {
        newHeight = Math.min(Game.height, screenHeight);
        newWidth = newHeight / 1.5;
        scaleUI = newHeight / Game.height;
    } else {
        newWidth = Math.min(Game.width, screenWidth);
        newHeight = newWidth * 1.5;
        scaleUI = newWidth / Game.width;
    }

    render.canvas.style.width = `${newWidth}px`;
    render.canvas.style.height = `${newHeight}px`;

    Game.elements.ui.style.width = `${Game.width}px`;
    Game.elements.ui.style.height = `${Game.height}px`;
    Game.elements.ui.style.transform = `scale(${scaleUI})`;
};

document.body.onload = resizeCanvas;
document.body.onresize = resizeCanvas;
