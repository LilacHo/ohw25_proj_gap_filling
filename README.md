# Mind the CHL Gap

Create a tutorial on gap-free Indian Ocean gridded data with U-Net method


The basic approach is the following:
```mermaid
graph LR
  A[netcdf/Zarr w time, lat, lon] --> G{to xarray}
  G --> C[standardized Zarr w masks and season]
  C --> D{CNN or UNet model}
  D --> E[Predict: xarray with gaps filled]
```

Functions are in `mindthegap` directory.
```
import mindthegap as mtg
```

## Collaborators

| Name                | Role                |
|---------------------|---------------------|
| [Eli Holmes](https://github.com/eeholmes)      | Project Facilitator |
| [Bruna Cândido](https://github.com/brunacandido)       | Fellow         |
| [Trina Xavier](https://github.com/trinaxavier2001)       | Participant         |
| [Lilac Hong](https://github.com/LilacHo) | Participant |



## Planning

* Initial idea: Create a tutorial on gap-free Indian Ocean gridded data with U-Net method
* [Pitch slide](https://docs.google.com/presentation/d/14JyNPC2JicP1IkHbWcDI0xt0FRbDmtdW4NTQo8wN80M/edit?slide=id.g37b3811c38a_11_5#slide=id.g37b3811c38a_11_5)
* Slack channel: ohw25_proj_gap
* repo: [https://github.com/oceanhackweek/ohw25_proj_gap](https://github.com/oceanhackweek/ohw25_proj_gap)
* [Final presentation](https://gamma.app/docs/Daily-Gap-Filled-Chlorophyll-a-Datasets-Using-Deep-Neural-Network-ozsc5xmxri96od1?mode=doc)

## Background
Chlorophyll is a widely used indicator of plankton abundance, and thus a key measure of marine productivity and ecosystem health, since the ocean covers nearly 70% of Earth’s surface. Estimating chlorophyll concentrations allows researchers to assess phytoplankton biomass, which supports oceanic food webs and contributes to global carbon cycling. Remote sensing with ocean-color instruments enables large-scale monitoring of chlorophyll-a by detecting the light reflectance of plankton. However, cloud cover continues to be a significant challenge, obstructing surface observations and creating gaps in chlorophyll-a data. These gaps limit our ability to monitor marine productivity accurately and to quantify the contribution of plankton to the global carbon cycle.

## Goals
Contribute to ["mind-the-chl-gap" project](https://github.com/ocean-satellite-tools/mind-the-chl-gap/tree/main) and the create a tutorial on gap-free Indian Ocean gridded data with U-Net method.
For OceanHackWeek 2025, we aimed to extend the existing work by exploring different types of CNN architectures and experimenting with alternative gap-filling tools, such as [segmentation_models_pytorch](https://github.com/qubvel-org/segmentation_models.pytorch), [DINCAE](https://github.com/gher-uliege/DINCAE.jl/tree/main).


## Datasets

```
import xarray as xr
dataset = xr.open_dataset(
    "gcs://nmfs_odp_nwfsc/CB/mind_the_chl_gap/IO.zarr",
    engine="zarr",
    backend_kwargs={"storage_options": {"token": "anon"}},
    consolidated=True
)
dataset
```

## Workflow/Roadmap
```mermaid
flowchart TD
    A[Zarr data] --> B[1_Data_Prep,ipynb]
    B --> C[2_U-Net_ModelFit.ipynb]
    C --> D[3_U-Net_Viz.ipynb]
```

## Directory Structure
```
ohw25_proj_gap_filling/
├── README.md
├── Note.md
├── mindthegap/
│   ├── __init__.py
│   ├── processing.py
│   ├── utils.py
|   ├── model.py
│   ├── viz.py
├── notebooks/
│   ├── 1_Data_Prep,ipynb
│   ├── 2_U-Net_ModelFit.ipynb
│   ├── 3_U-Net_Viz.ipynb
├── doc/
│   ├── plot_prediction_observed.png
│   ├── plot_prediction_gapfill.png
├── models/
│   ├── 2015_3_ArabSea/UNet_DoubleConv_mse.keras
└── book/
```

## Results/Findings
| <img width="623" alt="image" src="https://github.com/LilacHo/ohw25_proj_gap_filling/blob/main/doc/plot_prediction_gapfill.png"> | 
|:--:| 
| *Results from our U-Net model. Top left panel is the Copernicus Level-4 (science grade) Gap-filled Chl-a globColour product and Top right panel is our U-Net gap-filled product using the Copernicus Level-3 (gappy) data plus co-located environmental variables. The gap-filling algorithms are very different. Our model's ability to match a science-grade product is very promising. Note, we do not know that the globColour product doing better at gap-filling since we have no way to produce estimates from the globColour algorithm and compare to non-missing pixels, i.e. we cannot do our 'fake' clouds tests.* |

## Lessons Learned
* Working with outdated packages can be quite challenging.
* Existing frameworks (e.g., DINCAE) can serve as inspiration but need to be adapted to the specific context.
* Pay attention to memory efficiency — document how much memory is required to run your code and data.
* Collaboration and thorough documentation help improve workflow efficiency.
* Avoid using `to_numpy()` on the full dataset (time, lat, lon, var). Instead, stream patches directly from the Zarr files in batches or use [dask](https://www.dask.org/).
* Xarray is powerful, with advanced options available in [icechunk](https://github.com/earth-mover/icechunk) and [cubed](https://www.youtube.com/watch?v=HUFY2EFc6zs).

## References
* [PFT_gapfilling](https://github.com/EhsanMehdipour/PFT_gapfilling)



