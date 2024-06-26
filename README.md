# CSC475GroupProject
Group project repo for CSC475 course.

# Running the Project
Install requirements using the following:
```
pip install -r requirements.txt
```
It is recommended that a Python virtual environment is used.

Once requirements installed, run the notebook with:
```
jupyter notebook
```

# Dataset Used for Training
For training our model we used the guitar effects found in the IDMT-SFT-Audio-Effects dataset here: https://www.idmt.fraunhofer.de/en/publications/datasets/audio_effects.html [1].

The folder name expected is "dataset" followed by the following structure:
- dataset
    - experiments
        - *Used to store experiment results and wav files*
    - models
        - *Used to store .keras models that are made*
    - monophonic
        - *Monophonic 1 and 2 dataset contents which should have a "Lists" and a "Samples" folder**
    - polyphonic
        - *Polyphonic 1 and 2 (note effects are outisde the samples folder, so you must move them in) dataset contents which should have a "Lists" and a "Samples" folder*

# References
<div style="text-indent: -36px; padding-left: 36px;">
    <p>
        [1]&nbsp;&nbsp;&nbsp;&nbsp;M. Stein, “IDMT-SMT-Audio-Effects Dataset”. Zenodo, Jan. 17, 2023. doi: 10.5281/zenodo.7544032.
    </p>
</div>