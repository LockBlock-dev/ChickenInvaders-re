This repository contains all my work on reverse engineering the [Chicken Invaders](https://www.interactionstudios.com/chickeninvaders.php) game.

-   [assets.json](assets.json) - list of the game assets extracted from `ChickenInvaders.dat`
-   [unpack.py](unpack.py) - python script to list and extract the game assets
-   [patch.py](patch.py) - apply various patches to the game executable, available patches are:
    - windowed mode: force the game to run in windowed mode (prevents lags)
    - restore window style: set the window style to an overlapped window (what you would expect from a standard windowed window)

If you are using the patched executable, make sure to enable "Reduced color mode" and select "16-bit (65536) color" in the executable's compatibility tab.

You can also check the cheat I made for this game: [Omelette](https://github.com/LockBlock-dev/omelette).

## Disclaimer

This repository is for educational and research purposes only and is not affiliated with InterAction studios. InterAction studios retains all rights to the game and its assets, and we do not claim ownership or rights to any of the game content contained in this repository. By accessing this repository, you acknowledge and agree that you will not use any of the content for any unauthorized or illegal purposes.

## Copyright

See the [license](/LICENSE).
