# TIER Python

[![Latest Version on PyPi][ico-version]][link-pypi]
[![Software License][ico-license]](LICENSE.md)
[![Build Status][ico-github-actions]][link-github-actions]
[![Buy us a tree][ico-treeware-gifting]][link-treeware-gifting]

An SDK to easily work with the [TIER API](https://api-documentation.tier-services.io)

## Install

Via Pip

```shell
pip install tier-sdk
```

## Usage

```python
from tier import TIER

tier = TIER(api_token="your-token")

sites = tier.vehicles.in_radius(52.548977, 13.437837, 500)
```

| Available Methods                                      | Description                                                                                         |
|:-------------------------------------------------------|:----------------------------------------------------------------------------------------------------|
| `tier.vehicles.in_radius(latitude, longitude, radius)` | Retrieve a `VehiclesCollection` dict with details about vehicles for a specific radius.             |
| `tier.vehicles.in_zone(zone_id)`                       | Retrieve a `VehiclesCollection` dict with details about vehicles for a specific radius.             |
| `tier.vehicles.get(vehicle_id)`                        | Retrieve a `Vehicle` dict with details about a specific vehicle.                                    |
| `tier.zones.all()`                                     | Retrieve a `RootZonesCollection` dict with details about all zones.                                 |
| `tier.zones.near(latitude, longitude)`                 | Retrieve a `RootZonesCollection` dict with details about zones within 50km of a set of coordinates. |
| `tier.zones.get(zone_id)`                              | Retrieve a `RootZone` dict with details about a specific zone.                                      |

## Change log

Please see [CHANGELOG](CHANGELOG.md) for more information on what has changed recently.

## Testing

```shell
hatch shell

hatch run test
```

## Security

If you discover any security related issues, please email security@voke.dev instead of using the issue tracker.

## Credits

- [Owen Voke][link-author]
- [All Contributors][link-contributors]

## License

The MIT License (MIT). Please see [License File](LICENSE.md) for more information.

## Treeware

You're free to use this package, but if it makes it to your production environment you are required to buy the world a tree.

It’s now common knowledge that one of the best tools to tackle the climate crisis and keep our temperatures from rising above 1.5C is to plant trees. If you support this package and contribute to the Treeware forest you’ll be creating employment for local families and restoring wildlife habitats.

You can buy trees [here][link-treeware-gifting].

Read more about Treeware at [treeware.earth][link-treeware].

[ico-version]: https://img.shields.io/pypi/v/tier-sdk.svg?style=flat-square
[ico-license]: https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square
[ico-github-actions]: https://img.shields.io/github/actions/workflow/status/owenvoke/tier-python-sdk/tests.yml?branch=main&style=flat-square
[ico-treeware-gifting]: https://img.shields.io/badge/Treeware-%F0%9F%8C%B3-lightgreen?style=flat-square

[link-pypi]: https://pypi.org/project/tier-sdk
[link-github-actions]: https://github.com/owenvoke/tier-python-sdk/actions
[link-treeware]: https://treeware.earth
[link-treeware-gifting]: https://ecologi.com/owenvoke?gift-trees
[link-author]: https://github.com/owenvoke
[link-contributors]: https://github.com/owenvoke/tier-python-sdk/contributors
