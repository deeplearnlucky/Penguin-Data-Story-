import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import folium
from streamlit_folium import folium_static
import numpy as np
from sklearn.linear_model import LinearRegression
from folium.plugins import MarkerCluster
import plotly.graph_objects as go
import os
from datetime import datetime
import random


trend_model = LinearRegression()


# Set page config
st.set_page_config(
    layout="wide", page_title="Antarctic Penguin Population Dynamics", page_icon="🐧"
)

# Initialize session state if it doesn't exist
if "explored_sections" not in st.session_state:
    st.session_state.explored_sections = []

# Sidebar navigation
st.sidebar.title("🐧 Penguin Explorer")

# Custom CSS for the sidebar
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7bcf,#2e7bcf);
        color: white;
    }
    .sidebar .sidebar-content .stRadio > label {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
        transition: background-color 0.3s;
    }
    .sidebar .sidebar-content .stRadio > label:hover {
        background-color: rgba(255, 255, 255, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Emoji dictionary for sections
section_emojis = {
    "Introduction": "🏠",
    "Species Overview": "🔍",
    "Site Analysis": "🗺️",
    "Climate Impact": "🌡️",
    "Conservation": "🌿",
}

# Navigation with emojis and descriptions
st.sidebar.markdown("### Explore the Penguin World")

sections = [
    "Introduction",
    "Species Overview",
    "Site Analysis",
    "Climate Impact",
    "Conservation",
]

section_descriptions = {
    "Introduction": "Start your penguin journey",
    "Species Overview": "Meet the different penguin species",
    "Site Analysis": "Explore penguin habitats",
    "Climate Impact": "Understand environmental challenges",
    "Conservation": "Learn about protection efforts",
}

current_section = st.sidebar.radio(
    "Navigate to:",
    sections,
    format_func=lambda x: f"{section_emojis[x]} {x} - {section_descriptions[x]}",
)

# Add the current section to explored_sections if it's not already there
if current_section not in st.session_state.explored_sections:
    st.session_state.explored_sections.append(current_section)

# Fun fact in the sidebar
fun_facts = [
    "Emperor penguins can dive up to 1,800 feet deep!",
    "The smallest penguin species is only 16 inches tall.",
    "Some penguins can leap 6-9 feet out of the water!",
    "Penguins' black and white coloring is a form of camouflage called 'countershading'.",
    "Male emperor penguins incubate their eggs for two months without eating.",
]
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎉 Fun Penguin Fact")
st.sidebar.info(random.choice(fun_facts))

# Optional: Add a progress bar to show how far the user has explored
explored_sections = st.sidebar.multiselect(
    "Sections you've explored:",
    sections,
    # default=st.session_state.explored_sections,
    key="explored_sections",
)

progress = len(st.session_state.explored_sections) / len(sections)
st.sidebar.progress(progress)
st.sidebar.text(f"{int(progress * 100)}% explored")


st.markdown(
    """
<style>
    .stDataFrame {
        font-size: 0.8em;
    }
    .stDataFrame td {
        padding: 0.3em;
    }
</style>
""",
    unsafe_allow_html=True,
)


# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("./AllCounts_V_4_1.csv")
    return df


df = load_data()


# Load data
@st.cache_data
def load_climate_data():
    df = pd.read_csv(
        "Indicator_3_1_Climate_Indicators_Annual_Mean_Global_Surface_Temperature_577579683071085080.csv"
    )
    return df


df_climate = load_climate_data()


# Extract relevant data for Antarctica
antarctica_data = df_climate[df_climate["Country"] == "Antarctica"]

# Adjust the column names to fit the requirements
years = [str(year) for year in range(1961, 2024)]
temperature_data = antarctica_data[["Indicator"] + years].melt(
    id_vars=["Indicator"], var_name="year", value_name="temperature"
)


# Main content
st.title("Penguin Population Dynamics: A Journey Through Antarctic Colonies")

if current_section == "Introduction":
    st.header("Antarctic Penguin Population Dynamics")

    # Main introduction
    st.write(
        """
    Welcome to our Antarctic Penguin Population Dynamics Data Story!

    Imagine a world of ice and snow, where tuxedo-clad birds waddle across frozen landscapes and dive into icy waters. This is the realm of Antarctic penguins, and it's changing rapidly due to global climate shifts.

    Our story begins with a puzzling question: How are penguin populations responding to the warming Antarctic environment?
    """
    )

    # Image
    st.image(
        "./assets/ice.webp",
        caption="The cast of Arctic Circle by the cartoonist Alex Hallatt, includes three penguins, a polar bear, a lemming and a bunny.Credit...Alex Hallatt/King Features Syndicate",
        use_column_width=True,
    )

    # Key statistics
    st.subheader("Penguin Census")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Penguin Count", f"{df['penguin_count'].sum():,}")
    with col2:
        st.metric("Number of Species", df["common_name"].nunique())
    with col3:
        st.metric("Number of Sites", df["site_name"].nunique())

    # Detailed introduction
    st.write(
        """
    As we embark on this data-driven journey, we'll explore the lives of these remarkable birds, uncover surprising trends in their populations, and confront the challenges they face in a changing world. Are some penguin species thriving while others struggle? What does the future hold for these iconic Antarctic inhabitants?

    This interactive dashboard uses data from multiple sources to paint a comprehensive picture of Antarctic penguin populations:

    1. The Mapping Application for Penguin Populations and Projected Dynamics (MAPPPD), an open-access tool created by Oceanites, provides our core dataset on penguin populations and trends.

    2. The Palmer Archipelago (Antarctica) penguin dataset from Kaggle offers detailed information on penguin sizes and physical characteristics.

    3. Climate Change Data from the International Monetary Fund (IMF) allows us to examine carbon dioxide atmospheric concentrations, global warming trends, rising sea levels, and the frequency of natural disasters - key indicators for monitoring climate change and its impacts on penguin populations.

    Our exploration will take you through the fascinating world of Antarctic penguins, their population trends, and the challenges they face in a changing climate. We'll use advanced data analysis techniques, including linear regression, to uncover patterns and predict future trends.

    Penguins are not just adorable tuxedo-clad birds; they are also crucial indicators of the health of Antarctic and Southern Ocean ecosystems. By studying their populations, we gain valuable insights into the impacts of climate change, fishing activities, and other environmental factors on the delicate Antarctic ecosystem.
    """
    )

    # Interesting fact
    st.info(
        "Did you know? The total number of breeding pairs of penguins in the Antarctic region is estimated to be about 20 million! These penguins are concentrated in coastal regions, with some species, like the emperor penguins, huddling so closely in winter that they can reach a density of 19 birds per square metre."
    )

    # Wild vs Zoo Penguins
    st.subheader("Penguins in the Wild vs Zoos")
    wild_penguins = 40000000
    zoo_penguins = 4000

    fig = px.pie(
        values=[wild_penguins, zoo_penguins],
        names=["Wild", "Zoos"],
        title="Estimated Global Penguin Population Distribution",
    )
    st.plotly_chart(fig)

    st.write(
        f"""
    While our data shows an estimated {wild_penguins:,} penguins in the wild Antarctic regions, 
    it's reported that around {zoo_penguins:,} penguins from 11 species across five genera are 
    kept in domestic zoos and aquariums worldwide. This represents about a third of all penguins 
    in captivity globally.

    This means that for every penguin in captivity, there are approximately 
    {wild_penguins // zoo_penguins} penguins living in their natural habitats!
    
    It's important to note that these numbers are estimates and can fluctuate. Zoos play a crucial 
    role in conservation efforts, education, and research, but the vast majority of penguins 
    continue to thrive in their natural Antarctic environments.
    """
    )

    # Thesis statement
    st.write(
        """
    As we navigate through this dashboard, we'll address our central thesis: How are climate change and other environmental factors affecting different penguin species across various Antarctic sites, and what does this mean for the future of these iconic birds?
    """
    )

    # Explore Further
    st.subheader("Explore Further")
    st.write(
        """
    As you navigate through this dashboard, you'll discover:
    - Detailed information about different penguin species
    - Analysis of penguin populations across various Antarctic sites
    - The impact of climate change on penguin habitats
    - Conservation efforts and how you can contribute

    Join us as we dive into the data to uncover the story of Antarctica's penguins and explore how we can contribute to their conservation in the face of a changing climate.
    """
    )

    # Penguin Joke
    st.subheader("Penguin Humor")
    st.write(
        "Why don't you see penguins in Britain? Because they're afraid of Wales! 🐳😄"
    )

elif current_section == "Species Overview":
    st.header("Species Overview")
    st.write(
        """
As we delve deeper into our penguin tale, let's meet the main characters: the diverse penguin species that call Antarctica home. 

Each species has its own unique story, adapted to specific niches within the harsh Antarctic environment. But how do these adaptations fare in the face of climate change? 

Select a species below to uncover its secrets and see how it's faring in today's changing Antarctica.
"""
    )

    # Load the penguin size data
    @st.cache_data
    def load_size_data():
        return pd.read_csv("cleaned_penguins.csv")

    size_df = load_size_data()

    species = st.selectbox("Select a penguin species", size_df["species"].unique())

    st.subheader(f"About {species.title()} Penguins")

    species_info = {
        "Adelie": """
    # Adélie Penguin (Pygoscelis adeliae)

    ![Adélie Penguin](https://i.natgeofe.com/k/d3ea00a0-773b-437e-b7c6-a32f270b1b5a/adelie-penguin-jumping-ocean.jpg?wp=1&w=748&h=420)

    Adélie penguins are known for their distinctive tuxedo-like appearance and are found along the Antarctic coast. 
    Named after Adélie Land, these medium-sized penguins reach about 70 cm (28 inches) in height.

    ## Key Facts
    - **Diet**: 70% krill, 20% fish, 10% squid and other marine invertebrates
    - **Diving Depth**: Up to 175 meters
    - **Reproduction**: 2 eggs, 32-34 days incubation
    - **Chick Fledging**: 50-60 days
    - **Foraging Range**: Usually 10-15 km, up to 185 km during breeding season
    - **Temperature Preference**: -2°C to 2°C (28°F to 36°F)

    ## Conservation Status
    While still numerous, Adélie penguins face threats from climate change, affecting their sea ice habitat and food sources.

    > "Adélie penguins are the littlest and most widespread species of penguin in the Antarctic."
    """,
        "Chinstrap": """
    # Chinstrap Penguin (Pygoscelis antarcticus)

    ![Chinstrap Penguin](https://images.fineartamerica.com/images/artworkimages/mediumlarge/2/chinstrap-penguin-galaxiid.jpg)

    Chinstrap penguins are easily recognizable by the narrow black band under their heads. They inhabit the Antarctic Peninsula and several southern Atlantic islands.

    ## Key Facts
    - **Diet**: 95% krill, supplemented with small fish and squid
    - **Diving Depth**: Up to 70 meters
    - **Reproduction**: 2 eggs, 33-35 days incubation
    - **Chick Fledging**: 50-60 days
    - **Foraging Range**: Often within 60 km of breeding sites
    - **Temperature Preference**: 0°C to 4°C (32°F to 39°F)

    ## Conservation Status
    While not currently threatened, some populations have declined, possibly due to climate change impacts on their food supply.

    > "Chinstrap penguins can make over 1000 dives per day during breeding season!"
    """,
        "Gentoo": """
    # Gentoo Penguin (Pygoscelis papua)

    ![Gentoo Penguin](https://cdn.download.ams.birds.cornell.edu/api/v1/asset/612764627/2400)

    Gentoo penguins are the third largest penguin species, known for their bright orange-red bills and white patches behind their eyes. They have a wide distribution across sub-Antarctic islands and the Antarctic Peninsula.

    ## Key Facts
    - **Diet**: Varied - krill, squid, and fish
    - **Diving Depth**: Up to 200 meters
    - **Reproduction**: 2 eggs, 34-37 days incubation
    - **Chick Fledging**: 80-100 days
    - **Foraging Range**: Typically within 20 km of colony
    - **Temperature Preference**: -2°C to 10°C (28°F to 50°F)

    ## Conservation Status
    Near Threatened (IUCN). Some populations are stable or increasing, while others face threats from climate change and human activities.

    > "Gentoo penguins are the fastest underwater swimmers among penguins, reaching speeds up to 36 km/h (22 mph)!"
    """,
        "Macaroni": """
    # Macaroni Penguin (Eudyptes chrysolophus)

    ![Macaroni Penguin](https://preview.redd.it/to-boost-morale-pt-2-the-macaroni-penguin-v0-sd2mni06ue0a1.jpg?auto=webp&s=a27e82a545b447e83bfc0939c397fb3fe39cdcfb)

    Macaroni penguins are distinguished by their distinctive yellow crest feathers, reminiscent of the elaborate "macaroni" wigs popular in 18th-century Europe. They inhabit sub-Antarctic islands and the Antarctic Peninsula.

    ## Key Facts
    - **Diet**: 90% krill, supplemented with small fish and squid
    - **Diving Depth**: Up to 100 meters
    - **Reproduction**: 2 eggs laid, usually only 1 chick raised
    - **Incubation**: About 35 days
    - **Chick Fledging**: 60-70 days
    - **Foraging Range**: Up to 300 km from colonies
    - **Temperature Preference**: 2°C to 8°C (36°F to 46°F)

    ## Conservation Status
    Vulnerable (IUCN). Populations have declined by 30% or more since the 1970s, likely due to climate change and competition with commercial fisheries for krill.

    > "Macaroni penguins are the most numerous penguin species, with an estimated global population of 6.3 million breeding pairs!"
    """,
        "King": """
    # King Penguin (Aptenodytes patagonicus)

    ![King Penguin](https://live.staticflickr.com/65535/31327605330_8fbc10962a_3k.jpg)

    King penguins are the second largest penguin species, known for their striking yellow-orange neck patches. They inhabit sub-Antarctic islands around the Antarctic convergence.

    ## Key Facts
    - **Diet**: Mainly fish (particularly lanternfish) and squid
    - **Diving Depth**: Over 300 meters
    - **Reproduction**: 1 egg, unique 14-16 month breeding cycle
    - **Incubation**: About 55 days
    - **Chick Fledging**: 10-13 months
    - **Foraging Range**: Hundreds of kilometers, sometimes over 1000 km in a single trip
    - **Temperature Preference**: 2°C to 6°C (36°F to 43°F)

    ## Conservation Status
    Least Concern (IUCN). While currently stable, they face potential future threats from climate change.

    > "King penguin chicks have distinctive brown downy feathers, leading early explorers to think they were a separate species, which they named 'woolly penguins'!"
    """,
        "Emperor": """
    # Emperor Penguin (Aptenodytes forsteri)

    ![Emperor Penguin](https://www.thoughtco.com/thmb/xb_fSlautgdxRoIM5xUUDYk2Fmg=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/GettyImages-dv735012-0663e2057be948d1b8a906c8fdfa97a2.jpg)

    Emperor penguins are the largest of all penguin species, standing up to 1.2 meters (4 feet) tall. They are the only penguin species that breeds during the harsh Antarctic winter.

    ## Key Facts
    - **Diet**: Primarily fish and squid, with some krill
    - **Diving Depth**: Over 500 meters (deepest of any bird)
    - **Diving Duration**: Up to 20 minutes
    - **Reproduction**: 1 egg, laid in May or June
    - **Incubation**: About 65 days, male incubates on his feet
    - **Foraging Range**: Up to 1,500 km from breeding colonies
    - **Temperature Tolerance**: -60°C to -2°C (-76°F to 28°F)

    ## Conservation Status
    Near Threatened (IUCN). Particularly vulnerable to climate change due to their dependence on sea ice for breeding.

    > "Emperor penguins have the highest feather density of any bird species, with about 100 feathers per square inch, providing crucial insulation in their extreme environment!"
    """,
    }

    # Display species information
    if species in species_info:
        st.markdown(species_info[species])
    else:
        st.write("Information not available for this species.")

    # Filter data for the given species
    species_data = size_df[size_df["species"] == species]

    # Check if there is data available for the given species and relevant measurements are present
    if (
        not species_data.empty
        and species_data[
            ["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm", "body_mass_g"]
        ]
        .notnull()
        .any()
        .any()
    ):
        # Population trend chart
        st.subheader("Size Distribution")
        fig = px.box(
            species_data.dropna(
                subset=[
                    "culmen_length_mm",
                    "culmen_depth_mm",
                    "flipper_length_mm",
                    "body_mass_g",
                ]
            ),
            y=[
                "culmen_length_mm",
                "culmen_depth_mm",
                "flipper_length_mm",
                "body_mass_g",
            ],
            title=f"Size Distribution of {species} Penguins",
            labels={"value": "Measurement", "variable": "Attribute"},
        )
        st.plotly_chart(fig)

        # Size comparison
        st.subheader("Average Measurements")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Avg Body Mass (g)", f"{species_data['body_mass_g'].mean():.0f}")
        with col2:
            st.metric(
                "Avg Flipper Length (mm)",
                f"{species_data['flipper_length_mm'].mean():.1f}",
            )
        with col3:
            st.metric(
                "Avg Bill Length (mm)", f"{species_data['culmen_length_mm'].mean():.1f}"
            )
        with col4:
            st.metric(
                "Avg Bill Depth (mm)", f"{species_data['culmen_depth_mm'].mean():.1f}"
            )

        # Gender distribution
        st.subheader("Gender Distribution")
        gender_dist = (
            species_data["sex"]
            .map({0: "Unknown", 1: "Female", 2: "Male"})
            .value_counts()
        )
        fig = px.pie(
            values=gender_dist.values,
            names=gender_dist.index,
            title=f"Gender Distribution of {species} Penguins",
        )
        st.plotly_chart(fig)

        # Island distribution
        st.subheader("Island Distribution")
        island_dist = species_data["island"].value_counts()
        fig = px.bar(
            x=island_dist.index,
            y=island_dist.values,
            title=f"Distribution of {species} Penguins Across Islands",
        )
        st.plotly_chart(fig)

        # Correlation heatmap
        st.subheader("Correlation Between Measurements")
        corr = species_data[
            ["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm", "body_mass_g"]
        ].corr()
        fig = px.imshow(
            corr,
            text_auto=True,
            aspect="auto",
            title=f"Correlation Heatmap for {species} Penguins",
        )
        st.plotly_chart(fig)
    else:
        st.write("No data available for this species.")

    # Climate change impact
    st.subheader("Climate Change Impact")
    climate_impact = {
        "Adelie": """
        Adélie penguins are particularly vulnerable to climate change as they rely heavily on sea ice for breeding and foraging. 
        Warming temperatures are causing a decline in sea ice, which could significantly impact their population. Some key impacts include:
        
        1. Habitat loss: Reduced sea ice means less breeding and resting areas.
        2. Food scarcity: Changes in krill populations due to warming waters affect their primary food source.
        3. Increased competition: As ice-free areas increase, other penguin species may compete for Adélie territories.
        4. Breeding cycle disruption: Changes in seasonal patterns may affect their highly synchronized breeding cycle.
        
        Long-term studies have shown that some Adélie populations have declined by more than 65% over the past 25 years, largely attributed to climate change.
        """,
        "Chinstrap": """
        While chinstrap penguins are less dependent on sea ice than Adélies, they are still affected by climate change, primarily through 
        changes in their food supply. Key impacts include:
        
        1. Food web disruption: Warming waters affect krill populations, their primary food source.
        2. Range shifts: Some chinstrap populations are moving southward as temperatures warm.
        3. Breeding success: Changes in food availability can affect their ability to successfully raise chicks.
        4. Increased storms: Climate change may lead to more frequent and severe storms, which can impact breeding success.
        
        Some chinstrap populations have declined by up to 50% in recent decades, though the exact causes are still being studied.
        """,
        "Gentoo": """
        Gentoo penguins have shown some ability to adapt to warming temperatures, even expanding their range in some areas. However, they still 
        face challenges due to climate change:
        
        1. Range expansion: Gentoos are moving southward as waters warm, potentially competing with other penguin species.
        2. Changing diet: As fish populations shift due to warming waters, gentoos may need to adapt their diet.
        3. Breeding habitat changes: Increased rainfall and earlier spring melts can flood nesting sites.
        4. Potential benefits: Ice-free areas becoming available might provide new nesting grounds for gentoos.
        
        While some gentoo populations are stable or increasing, others face declines. Their adaptability may make them more resilient to climate 
        change compared to other penguin species, but they are still at risk.
        """,
        "Macaroni": """
        Macaroni penguins face several challenges due to climate change:
        1. Food availability: Warming waters affect krill populations, their primary food source.
        2. Breeding habitat: Rising sea levels and increased rainfall can flood nesting sites.
        3. Ocean acidification: This may impact the food chain, affecting the availability of their prey.
        4. Range shifts: Macaronis may need to move to new areas as water temperatures change.

        Some Macaroni penguin populations have declined by over 50% since the 1970s, partly due to climate change impacts.
        """,
        "King": """
        King penguins are vulnerable to climate change in several ways:
        1. Foraging grounds: Warming oceans may shift the Antarctic Polar Front, forcing king penguins to travel further to find food.
        2. Breeding cycle: Their long breeding cycle makes them sensitive to year-to-year environmental changes.
        3. Habitat loss: Rising sea levels threaten to inundate some of their breeding beaches.
        4. Food web changes: Alterations in fish distributions due to warming waters could affect their prey availability.

        While currently stable, some models predict significant population declines for king penguins if warming trends continue.
        """,
        "Emperor": """
        Emperor penguins are highly vulnerable to climate change:
        1. Sea ice loss: They depend on stable sea ice for breeding, which is rapidly declining in some areas.
        2. Breeding failure: Early sea ice breakup can cause catastrophic breeding failures.
        3. Food availability: Changes in sea ice affect their prey species.
        4. Habitat loss: Some colonies may need to relocate as their traditional breeding grounds become unsuitable.

        Studies predict that if current warming trends continue, more than 50% of emperor penguins could decline or disappear by 2100.
        """,
    }
    st.write(
        climate_impact.get(
            species, "Climate change impact information not available for this species."
        )
    )

    # Conservation efforts
    st.subheader("Conservation Efforts")
    conservation_info = {
        "Adelie": """
        Conservation efforts for Adélie penguins include:
        1. Establishing Marine Protected Areas (MPAs) in the Southern Ocean to protect their habitat and food sources.
        2. Long-term monitoring programs to track population trends and health.
        3. Regulating tourism to minimize disturbance to breeding colonies.
        4. Supporting international agreements to mitigate climate change and protect Antarctic ecosystems.
        5. Research into potential climate change refugia where Adélie populations might persist in the face of warming temperatures.
        """,
        "Chinstrap": """
        Conservation efforts for Chinstrap penguins include:
        1. Monitoring programs to track population trends across their range.
        2. Studies on krill populations and fisheries management to ensure sustainable food sources.
        3. Efforts to minimize disturbance from tourism and research activities.
        4. Inclusion in broader Antarctic conservation plans and protected areas.
        5. Research into the impacts of climate change on their breeding and foraging habitats.
        """,
        "Gentoo": """
        Conservation efforts for Gentoo penguins include:
        1. Establishment and management of protected areas where they breed.
        2. Monitoring programs to track population trends and health across their range.
        3. Management of introduced predators on some sub-Antarctic islands where they breed.
        4. Sustainable fisheries management to ensure food availability.
        5. Research into their adaptability to changing environmental conditions to inform future conservation strategies.
        """,
        "Macaroni": """
        Conservation efforts for Macaroni penguins include:
        1. Establishing Marine Protected Areas in their foraging grounds.
        2. Regulating krill fisheries to ensure sustainable food sources.
        3. Monitoring programs to track population trends and health.
        4. Research into their adaptability to changing environmental conditions.
        5. Efforts to minimize disturbance from human activities on their breeding islands.
        """,
        "King": """
        Conservation efforts for King penguins include:
        1. Protecting breeding habitats on sub-Antarctic islands.
        2. Long-term monitoring programs to track population trends.
        3. Research into the impacts of climate change on their foraging patterns.
        4. Management of introduced predators on some breeding islands.
        5. Efforts to minimize disturbance from tourism and research activities.
        """,
        "Emperor": """
        Conservation efforts for Emperor penguins include:
        1. Proposals to list them under the Endangered Species Act for additional protections.
        2. Extensive research and monitoring programs to track population trends and breeding success.
        3. Efforts to establish Marine Protected Areas in the Southern Ocean.
        4. Climate change mitigation efforts, as this is their primary threat.
        5. Careful management of human activities in Antarctica to minimize disturbance.
        """,
    }
    st.write(
        conservation_info.get(
            species, "Conservation information not available for this species."
        )
    )

elif current_section == "Site Analysis":
    st.header("Site Analysis")
    st.write(
        """
Our journey now takes us across the vast Antarctic landscape, from windswept islands to icy continental shores. These diverse sites are the stages upon which our penguin drama unfolds.

As we explore these locations, a central question emerges: Are all penguin habitats equally affected by climate change, or are some sites serving as refuges while others face decline?

Let's dive into the data and uncover the geographic patterns of penguin population dynamics.
"""
    )

    # Load and preprocess data
    @st.cache_data
    def load_site_data():
        site_data = (
            df.groupby(
                [
                    "site_name",
                    "latitude_epsg_4326",
                    "longitude_epsg_4326",
                    "common_name",
                ]
            )["penguin_count"]
            .sum()
            .reset_index()
        )
        site_data["total_count"] = site_data.groupby("site_name")[
            "penguin_count"
        ].transform("sum")
        return site_data

    site_data = load_site_data()

    st.subheader("Penguin Colony Locations")

    # Dark mode toggle, default is True (dark mode)
    dark_mode = st.toggle("Light Mode", value=False)

    # Choose tile based on dark mode
    tile = "CartoDB positron" if dark_mode else "CartoDB dark_matter"

    m = folium.Map(location=[-77, 0], zoom_start=3, tiles=tile)

    # Create a MarkerCluster
    marker_cluster = MarkerCluster()

    epsilon = 1e-10

    # Add markers for each unique site, with size based on population
    for _, site in site_data.drop_duplicates("site_name").iterrows():
        total_count = site["total_count"] + epsilon  # Add epsilon to avoid log(0)
        radius = np.log(total_count) * 2  # Adjust size based on population

        folium.CircleMarker(
            location=[site["latitude_epsg_4326"], site["longitude_epsg_4326"]],
            radius=radius,
            popup=f"<b>{site['site_name']}</b><br>Total Penguin Count: {site['total_count']:,}",
            color="lightblue" if not dark_mode else "blue",
            fill=True,
            fill_color="lightblue" if not dark_mode else "blue",
            fill_opacity=0.7,
            weight=2,
        ).add_to(marker_cluster)

    marker_cluster.add_to(m)

    # Add a legend
    legend_html = f"""
    <div style="position: fixed; bottom: 50px; left: 50px; width: 120px; height: 90px; 
        border:2px solid grey; z-index:9999; font-size:14px;
        background-color:rgba({255 if dark_mode else 0}, {255 if dark_mode else 0}, {255 if dark_mode else 0}, 0.8);">
        <p style="margin-top: 5px; margin-bottom: 5px; margin-left: 5px; color: {'black' if dark_mode else 'white'};">
        <strong>Legend</strong><br>
        • Small Colony<br>
        •• Medium Colony<br>
        ••• Large Colony
        </p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # Display the map
    folium_static(m, width=800, height=600)

    st.write(
        """
    This map shows the locations of various penguin colonies across Antarctica. 
    Each blue circle represents a unique site where penguin populations have been observed and counted. 
    The size of the circle is proportional to the total penguin population at that site.
    Click on a circle to see the site name and the total penguin count at that location.
    """
    )

    # Selector for number of top sites
    num_top_sites = st.slider(
        "Select number of top sites to display", min_value=3, max_value=20, value=10
    )
    top_sites = (
        site_data.drop_duplicates("site_name")
        .nlargest(num_top_sites, "total_count")["site_name"]
        .tolist()
    )

    # Top N Sites by Population
    st.subheader(f"Top {num_top_sites} Penguin Colony Sites")
    top_n_sites = site_data.drop_duplicates("site_name").nlargest(
        num_top_sites, "total_count"
    )

    fig = px.bar(
        top_n_sites,
        x="site_name",
        y="total_count",
        title=f"Top {num_top_sites} Penguin Colony Sites by Population",
        labels={"site_name": "Site Name", "total_count": "Total Penguin Count"},
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)

    st.write(
        f"""
    This bar chart shows the top {num_top_sites} penguin colony sites by total population. 
    These sites are crucial for penguin conservation efforts due to their large populations.
    """
    )

    # Species Distribution across Top N Sites
    st.subheader(f"Species Distribution in Top {num_top_sites} Sites")
    species_dist = site_data[site_data["site_name"].isin(top_sites)]

    fig = px.bar(
        species_dist,
        x="site_name",
        y="penguin_count",
        color="common_name",
        title=f"Species Distribution in Top {num_top_sites} Penguin Colony Sites",
        labels={
            "site_name": "Site Name",
            "penguin_count": "Penguin Count",
            "common_name": "Species",
        },
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)

    st.write(
        f"""
    This stacked bar chart shows the distribution of different penguin species across the top {num_top_sites} colony sites.
    It provides insights into which species are dominant at each site and the overall diversity of penguins at these locations.
    """
    )

    # Site Comparison
    st.subheader("Site Comparison")
    selected_sites = st.multiselect(
        "Select sites to compare", df["site_name"].unique(), default=top_sites
    )

    if selected_sites:
        # Filter data for selected sites
        comparison_data = df[df["site_name"].isin(selected_sites)]

        # Create a line chart for each species at the selected sites
        chart = (
            alt.Chart(comparison_data)
            .mark_line()
            .encode(
                x="year:O",
                y="penguin_count:Q",
                color="common_name:N",
                strokeDash="site_name:N",
                tooltip=["site_name", "common_name", "year", "penguin_count"],
            )
            .properties(width=800, height=400)
            .interactive()
        )

        st.altair_chart(chart, use_container_width=True)

    # Summary statistics
    st.subheader("Summary Statistics")

    if selected_sites:
        # Calculate summary statistics
        summary = (
            comparison_data.groupby("site_name")
            .agg({"penguin_count": ["mean", "min", "max"], "year": ["min", "max"]})
            .reset_index()
        )
        summary.columns = [
            "Site",
            "Avg Count",
            "Min Count",
            "Max Count",
            "First Year",
            "Last Year",
        ]

        # Calculate trend for each site
        for site in selected_sites:
            site_trend = (
                comparison_data[comparison_data["site_name"] == site]
                .groupby("year")["penguin_count"]
                .sum()
                .reset_index()
            )
            trend_model = LinearRegression()
            trend_model.fit(site_trend[["year"]], site_trend["penguin_count"])
            summary.loc[summary["Site"] == site, "Trend"] = trend_model.coef_[0]

        # Function to color code the trends
        def color_trend(val):
            if pd.isna(val):
                return "color: black"
            elif val > summary["Avg Count"].mean():
                return "color: green"
            else:
                return "color: red"

        # Apply styling
        styled_summary = summary.style.map(
            color_trend, subset=["Avg Count", "Min Count", "Max Count"]
        )

        # Display the styled dataframe
        st.dataframe(
            styled_summary.format(
                {
                    "Avg Count": "{:,.0f}",
                    "Min Count": "{:,.0f}",
                    "Max Count": "{:,.0f}",
                    "First Year": "{:.0f}",
                    "Last Year": "{:.0f}",
                    "Trend": "{:.2f}",
                }
            ),
        )

        # Add explanatory text
        st.markdown(
            """
        * **Green** values indicate above-average counts
        * **Red** values indicate below-average counts
        * **Trend** shows the slope (population change per year) of the linear regression line (positive for increasing, negative for decreasing)
        """
        )
        # Add custom CSS to adjust table size
        st.markdown(
            """
        <style>
        .summary-stats-table {
            font-size: 0.8em;  /* Adjust font size */
        }
        .summary-stats-table td {
            padding: 0.3em;  /* Adjust cell padding */
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

        # Calculate and display additional statistics
        total_penguins = summary["Max Count"].sum()
        total_years = summary["Last Year"].max() - summary["First Year"].min()
        avg_penguins_per_site = summary["Avg Count"].mean()

        st.markdown(
            f"""
        ### Key Insights:
        - Total penguins across all selected sites: **{total_penguins:,}**
        - Years of data collection: **{total_years:.0f}**
        - Average penguins per site: **{avg_penguins_per_site:,.0f}**
        """
        )

        # Trend analysis
        st.subheader("Population Trend Analysis")
        for site in selected_sites:
            site_trend = (
                comparison_data[comparison_data["site_name"] == site]
                .groupby("year")["penguin_count"]
                .sum()
                .reset_index()
            )
            trend_model = LinearRegression()
            trend_model.fit(site_trend[["year"]], site_trend["penguin_count"])
            trend = "increasing" if trend_model.coef_[0] > 0 else "decreasing"
            trend_strength = abs(trend_model.coef_[0])

            if trend_strength > 100:
                strength = "strong"
            elif trend_strength > 50:
                strength = "moderate"
            else:
                strength = "slight"

            st.markdown(
                f"- The overall population trend at **{site}** is **{strength}ly {trend}**."
            )

        st.write(
            """
        This interactive chart allows you to compare penguin populations across different sites and species. 
        Select multiple sites from the dropdown menu to visualize their population trends over time. 
        The summary statistics provide a quick overview of the average, minimum, and maximum penguin counts 
        for each selected site, as well as the range of years for which data is available.
        
        Key observations:
        - Population fluctuations: Notice how penguin numbers can vary significantly from year to year at a single site.
        - Species distribution: Some sites may host multiple penguin species, while others are dominated by a single species.
        - Long-term trends: Look for overall increases or decreases in population over extended periods.
        
        These patterns can be influenced by factors such as climate change, food availability, and human activities. 
        Continued monitoring of these sites is crucial for understanding and protecting Antarctic penguin populations.
        """
        )

    # Additional Insights
    st.subheader("Additional Insights")

    # Species Richness
    species_richness = (
        df.groupby("site_name")["common_name"].nunique().sort_values(ascending=False)
    )
    st.write(
        f"The site with the highest species richness is {species_richness.index[0]} with {species_richness.iloc[0]} different penguin species."
    )

    # Most Stable Population
    population_stability = (
        df.groupby("site_name")["penguin_count"].std()
        / df.groupby("site_name")["penguin_count"].mean()
    )
    most_stable_site = population_stability.sort_values().index[0]
    st.write(
        f"The site with the most stable penguin population over time is {most_stable_site}."
    )

    # Largest Single-Year Change
    df["year"] = pd.to_datetime(df["year"], format="%Y")
    df["year_diff"] = df.groupby("site_name")["year"].diff().dt.days / 365.25
    df["annual_change"] = (
        df.groupby("site_name")["penguin_count"].diff() / df["year_diff"]
    )
    largest_change = df.loc[df["annual_change"].abs().idxmax()]
    st.write(
        f"The largest single-year change in penguin population occurred at {largest_change['site_name']} between {largest_change['year'].year - 1} and {largest_change['year'].year}, with a change of {largest_change['annual_change']:.0f} penguins per year."
    )

    # Conservation Implications
    st.subheader("Conservation Implications")
    st.write(
        """
    Based on the site analysis, we can draw several important conclusions for penguin conservation:

    1. Priority Sites: The top 10 sites by population should be given high priority in conservation efforts due to their importance for overall penguin numbers.
    
    2. Species Diversity: Sites with high species richness are important for maintaining overall penguin diversity and should be protected.
    
    3. Population Stability: Sites with stable populations may provide insights into favorable conditions for penguins and could be used as models for conservation efforts at other sites.
    
    4. Rapid Changes: Sites experiencing large population changes should be closely monitored to understand the causes of these fluctuations and to implement appropriate conservation measures.
    
    5. Long-term Monitoring: Continued long-term monitoring of all sites is crucial for understanding population trends and the effects of climate change on penguin populations.
    
    6. Habitat Protection: Conservation efforts should focus on protecting not just the breeding sites, but also the surrounding marine areas that are crucial for penguin foraging.
    
    These insights can help guide conservation strategies and resource allocation for penguin protection in Antarctica.
    """
    )

elif current_section == "Climate Impact":
    st.header("Climate Impact")
    st.write(
        """
We've met our penguin protagonists and explored their homes. Now, we face the rising conflict in our story: the impact of climate change.

As temperatures rise and ice melts, how are penguin populations responding? Are we witnessing a tragedy unfolding, or a tale of remarkable resilience?

Let's examine the data to uncover the intricate relationship between climate trends and penguin numbers. What we find may challenge our expectations and reveal surprising twists in the penguin saga.
"""
    )
    st.subheader("Temperature Trends in Antarctica")

    # Ensure temp_data is properly formatted
    temp_data = temperature_data.groupby("year")["temperature"].mean().reset_index()
    temp_data["year"] = temp_data["year"].astype(int)

    # Perform linear regression on temperature data
    X = temp_data["year"].values.reshape(-1, 1)
    y = temp_data["temperature"].values
    model = LinearRegression()
    model.fit(X, y)

    # Create prediction line
    X_pred = np.array([temp_data["year"].min(), temp_data["year"].max()]).reshape(-1, 1)
    y_pred = model.predict(X_pred)

    fig = px.line(
        temp_data,
        x="year",
        y="temperature",
        title="Average Annual Temperature in Antarctica",
    )
    fig.add_traces(
        px.line(x=X_pred.flatten(), y=y_pred, color_discrete_sequence=["red"]).data
    )

    fig.update_layout(
        yaxis=dict(title="Temperature (°C)"),
        xaxis=dict(title="Year"),
        hovermode="x unified",
        legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=0),
    )

    fig.update_traces(hovertemplate="Year: %{x}<br>Temperature: %{y:.2f}°C")

    # Update legend
    fig.data[0].name = "Actual Temperature"
    fig.data[1].name = "Linear Trend"

    st.plotly_chart(fig)

    # Calculate and display trend information
    temp_trend = model.coef_[0]
    temp_intercept = model.intercept_
    r_squared = model.score(X, y)

    st.write(
        f"""
    #### Key observations:
    - The lowest recorded average temperature was {temp_data['temperature'].min():.2f}°C in {temp_data.loc[temp_data['temperature'].idxmin(), 'year']}.
    - The highest recorded average temperature was {temp_data['temperature'].max():.2f}°C in {temp_data.loc[temp_data['temperature'].idxmax(), 'year']}.
    - There is a clear warming trend visible over the years.
    - The linear regression analysis shows:
        - Temperature is increasing at a rate of {temp_trend:.4f}°C per year.
        - The R-squared value is {r_squared:.4f}, indicating that {r_squared*100:.1f}% of the temperature variation can be explained by the passing of time.
    - If this trend continues, we could expect an increase of {temp_trend*10:.2f}°C over the next decade.
    """
    )

    # Total Penguin Population vs Temperature
    st.subheader("Total Penguin Population vs Temperature")

    total_penguin_data = df.groupby("year")["penguin_count"].sum().reset_index()
    total_penguin_data["year"] = total_penguin_data["year"].astype(int)

    merged_data = pd.merge(total_penguin_data, temp_data, on="year", how="inner")

    # Perform linear regression on penguin data
    X_penguin = merged_data["year"].values.reshape(-1, 1)
    y_penguin = merged_data["penguin_count"].values
    model_penguin = LinearRegression()
    model_penguin.fit(X_penguin, y_penguin)

    # Create prediction line for penguin population
    X_pred_penguin = np.array(
        [merged_data["year"].min(), merged_data["year"].max()]
    ).reshape(-1, 1)
    y_pred_penguin = model_penguin.predict(X_pred_penguin)

    fig = go.Figure()

    # Add temperature data
    fig.add_trace(
        go.Scatter(
            x=merged_data["year"],
            y=merged_data["temperature"],
            name="Temperature",
            line=dict(color="red"),
        )
    )

    # Add penguin count data
    fig.add_trace(
        go.Scatter(
            x=merged_data["year"],
            y=merged_data["penguin_count"],
            name="Penguin Count",
            yaxis="y2",
            line=dict(color="blue"),
        )
    )

    # Add linear regression for temperature
    fig.add_trace(
        go.Scatter(
            x=X_pred.flatten(),
            y=y_pred,
            name="Temperature Trend",
            line=dict(color="orange", dash="dash"),
        )
    )

    # Add linear regression for penguin count
    fig.add_trace(
        go.Scatter(
            x=X_pred_penguin.flatten(),
            y=y_pred_penguin,
            name="Penguin Count Trend",
            yaxis="y2",
            line=dict(color="green", dash="dash"),
        )
    )

    fig.update_layout(
        title="Temperature and Total Penguin Population Over Time",
        xaxis=dict(title="Year"),
        yaxis=dict(title="Temperature (°C)", color="red"),
        yaxis2=dict(
            title="Total Penguin Count", overlaying="y", side="right", color="blue"
        ),
        legend=dict(x=1.1, y=1, bgcolor="rgba(255, 255, 255, 0.5)"),
        hovermode="x unified",
    )

    st.plotly_chart(fig)

    # Calculate and display trend information for penguin population
    penguin_trend = model_penguin.coef_[0]
    penguin_intercept = model_penguin.intercept_
    r_squared_penguin = model_penguin.score(X_penguin, y_penguin)

    st.write(
        f"""
    #### Key observations:
    1. Temperature Trend:
    - Temperature is increasing at a rate of {temp_trend:.4f}°C per year.
    - The R-squared value for temperature is {r_squared:.4f}.

    2. Penguin Population Trend:
    - The penguin population is changing at a rate of {penguin_trend:.0f} individuals per year.
    - The R-squared value for penguin population is {r_squared_penguin:.4f}.
    - If this trend continues, we could expect a change of {penguin_trend*10:.0f} individuals over the next decade.

    3. Potential Correlations:
    - The relationship between temperature and penguin population is complex.
    - While both show overall increasing trends, the penguin population shows more fluctuation.
    - This suggests that factors other than temperature also play significant roles in penguin population dynamics.
    """
    )

    st.subheader("Penguin Population Trends by Species")
    species = st.selectbox("Select a species", df["common_name"].unique())
    species_data = (
        df[df["common_name"] == species]
        .groupby("year")["penguin_count"]
        .sum()
        .reset_index()
    )
    species_data["year"] = species_data["year"].astype(int)

    # Filter temperature data to match the range of penguin data
    min_year = species_data["year"].min()
    max_year = species_data["year"].max()
    filtered_temp_data = temp_data[
        (temp_data["year"] >= min_year) & (temp_data["year"] <= max_year)
    ]

    # Perform linear regression on species data
    X_species = species_data["year"].values.reshape(-1, 1)
    y_species = species_data["penguin_count"].values
    model_species = LinearRegression()
    model_species.fit(X_species, y_species)

    # Create prediction line for species population
    X_pred_species = np.array(
        [species_data["year"].min(), species_data["year"].max()]
    ).reshape(-1, 1)
    y_pred_species = model_species.predict(X_pred_species)

    # Perform linear regression on filtered temperature data
    X_temp = filtered_temp_data["year"].values.reshape(-1, 1)
    y_temp = filtered_temp_data["temperature"].values
    model_temp = LinearRegression()
    model_temp.fit(X_temp, y_temp)
    y_pred_temp = model_temp.predict(X_pred_species)

    fig = go.Figure()

    # Add temperature data
    fig.add_trace(
        go.Scatter(
            x=filtered_temp_data["year"],
            y=filtered_temp_data["temperature"],
            name="Temperature",
            line=dict(color="red"),
        )
    )

    # Add species count data
    fig.add_trace(
        go.Scatter(
            x=species_data["year"],
            y=species_data["penguin_count"],
            name=f"{species} Count",
            yaxis="y2",
            line=dict(color="blue"),
        )
    )

    # Add linear regression for temperature
    fig.add_trace(
        go.Scatter(
            x=X_pred_species.flatten(),
            y=y_pred_temp,
            name="Temperature Trend",
            line=dict(color="orange", dash="dash"),
        )
    )

    # Add linear regression for species count
    fig.add_trace(
        go.Scatter(
            x=X_pred_species.flatten(),
            y=y_pred_species,
            name=f"{species} Count Trend",
            yaxis="y2",
            line=dict(color="green", dash="dash"),
        )
    )

    fig.update_layout(
        title=f"Temperature and {species.title()} Population Over Time",
        xaxis=dict(title="Year"),
        yaxis=dict(title="Temperature (°C)", color="red"),
        yaxis2=dict(
            title=f"{species.title()} Count", overlaying="y", side="right", color="blue"
        ),
        legend=dict(x=1.1, y=1, bgcolor="rgba(255, 255, 255, 0.5)"),
        hovermode="x unified",
    )

    st.plotly_chart(fig)

    # Calculate and display trend information for species population
    species_trend = model_species.coef_[0]
    species_intercept = model_species.intercept_
    r_squared_species = model_species.score(X_species, y_species)

    temp_trend = model_temp.coef_[0]
    r_squared_temp = model_temp.score(X_temp, y_temp)

    st.write(
        f"""
    The chart for {species} reveals species-specific responses to temperature changes:
    
    1. Temperature Trend: 
    - Temperature is changing at a rate of {temp_trend:.4f}°C per year for this period.
    - The R-squared value for the temperature trend is {r_squared_temp:.4f}.
    
    2. Population Trend: 
    - The {species} population is changing at a rate of {species_trend:.0f} individuals per year.
    - The R-squared value for the {species} population trend is {r_squared_species:.4f}.
    - If this trend continues, we could expect a change of {species_trend*10:.0f} {species} penguins over the next decade.
    
    3. Temperature Sensitivity: 
    - {species.title()} penguins appear to be {'particularly sensitive' if abs(species_trend) > 1000 else 'somewhat responsive'} 
    to temperature changes, with {'noticeable changes correlating with temperature fluctuations' if r_squared_species > 0.5 else 'varying responses to temperature fluctuations'}.
    
    4. Recent Trends: 
    - In the last decade, we observe {'a decline' if species_trend < 0 else 'an increase'} in {species} numbers, 
    which {'correlates with the continued warming trend' if r_squared_species > 0.5 else 'may be influenced by various environmental factors'}.
    
    This species-specific analysis highlights the importance of considering individual species' responses to climate change, 
    as different penguin species may have varying adaptabilities and ecological niches.
    """
    )

    st.subheader("Interpreting the Climate-Penguin Relationship")

    st.write(
        """
    When analyzing the relationship between climate change and penguin populations, several key factors must be considered:

    1. Direct and Indirect Effects: 
    - Direct: Changes in air temperature can affect penguins' thermal regulation and breeding conditions.
    - Indirect: Climate change influences sea ice extent, which critically impacts breeding habitats and food availability.
    """
    )
    col1, col2 = st.columns(2)
    with col1:
        st.image(
            "https://ichef.bbci.co.uk/news/1536/cpsprodpb/2FE2/production/_130885221_smyley_island_penguin_s2_layout-2x-nc.png.webp",
            caption="Loss of Smyley Island emperor colony in 2022 due to sea ice breakup. Source: Copernicus Sentinel-2",
            use_column_width=True,
        )

    st.write(
        """
    This image sequence dramatically illustrates the rapid loss of sea ice at the Smyley Island emperor penguin colony in 2022:

    - On October 21, the colony was visible on stable sea ice.
    - By October 28, open water had already appeared, fragmenting the ice.
    - By December 3, the entire area had become open water with floating ice, likely resulting in the loss of all chicks at this colony.

    This visual evidence underscores the immediate and devastating impact of climate change on emperor penguin breeding grounds.
    """
    )
    col1, col2 = st.columns(2)
    with col1:
        st.image(
            "https://ichef.bbci.co.uk/news/1536/cpsprodpb/6264/production/_130788152_antarctic_sea_ice_bellingshausen_mapv2-2x-nc.png.webp",
            caption="Sea-ice concentration on 15 November 2022, showing significant missing ice in key areas for penguin colonies. Source: NSIDC, Polar Bremen",
            use_column_width=True,
        )

    st.write(
        """
    2. Species-Specific Responses:
    - Different penguin species have varying tolerances to temperature changes and adaptabilities to changing environments.
    - Emperor penguins are particularly vulnerable due to their reliance on stable sea ice for breeding.
    - The image above shows the sea-ice concentration in November 2022, with the yellow dotted line indicating the median ice extent from 1981-2010. The significant reduction in sea ice, especially in the Bellingshausen Sea area, directly affects penguin habitats.
    - A catastrophic die-off of up to 10,000 emperor penguin chicks was observed in late 2022 in the Bellingshausen Sea area due to this early sea ice breakup.
    """
    )
    col1, col2 = st.columns(2)
    with col1:
        st.image(
            "https://ichef.bbci.co.uk/news/1536/cpsprodpb/FD0C/production/_130808746_emperor_penguin_cycle_v2_2x640-nc.png.webp",
            caption="Emperor penguin breeding cycle and its dependence on sea-ice. Source: PN Trathan/B Winecke",
            use_column_width=True,
        )

    st.write(
        """
    3. Ecological Cascade Effects:
    - As shown in the breeding cycle image, emperor penguins depend on stable sea ice for over 8 months of the year for breeding and chick rearing.
    - Changes in temperature and sea ice affect not just breeding but the entire Antarctic food web, from phytoplankton to krill to fish.
    - Penguins, as top predators, are impacted by changes at all levels of this food web.

    4. Time Lags and Long-Term Trends:
    - As seen in the Smyley Island case, the effects of climate change on penguin populations can be sudden and catastrophic.
    - Long-term data collection and satellite monitoring are crucial for understanding population trends and their correlation with climate variables.
    """
    )
    col1, col2 = st.columns(2)
    with col1:
        st.image(
            "https://ichef.bbci.co.uk/news/1536/cpsprodpb/11DF9/production/_130890237_antarctic_sea_ice_extent_24aug2023-nc.png.webp",
            caption="Antarctic sea-ice extent from 1979-2023, showing lower than usual levels in recent years. Source: National Snow and Ice Data Center (NSIDC)",
            use_column_width=True,
        )

    st.write(
        """
    - This graph shows the daily sea-ice extent in Antarctica from 1979 to 2023. The blue line representing 2023 shows significantly lower sea-ice extent compared to previous years.
    - Recent studies predict that more than 90% of emperor penguin colonies could be all but extinct by the end of the century if current warming trends continue.

    5. Regional Variations:
    - Climate change impacts can vary across different regions of Antarctica.
    - In 2022, four out of five observed emperor penguin colonies in the Bellingshausen Sea sector, including Smyley Island, suffered total breeding failure due to early ice breakup.

    6. Human Factors and Conservation Efforts:
    - Increased human activity in Antarctica, including tourism and research, may also influence penguin populations.
    - Conservation efforts, such as establishing Marine Protected Areas and regulating tourism, can help mitigate some climate change impacts.
    - Proposals have been made to list emperor penguins as "Vulnerable" on the IUCN Red List due to climate change threats.

    7. Resilience and Adaptation:
    - While some penguin populations may show resilience, the rapid pace of change seen at Smyley Island suggests adaptation may be challenging for many colonies.
    - Continuous monitoring of these adaptations is crucial for predicting future population trends and informing conservation strategies.

    In conclusion, these images and data present clear and alarming evidence of the impact of climate change on Antarctic sea ice and penguin populations. The relationship is complex and multifaceted, with potentially devastating consequences for some species, particularly emperor penguins.

    The catastrophic events observed in 2022, where thousands of emperor penguin chicks perished due to early ice breakup, serve as a stark warning of the immediate threats posed by climate change. This is not just a future scenario, but a present reality for these iconic Antarctic inhabitants.

    Continued long-term monitoring, coupled with comprehensive ecological studies, is essential for fully understanding and predicting the future of Antarctic penguin populations in the face of ongoing climate change. This understanding is crucial for developing effective conservation strategies to protect these iconic species and the unique Antarctic ecosystem they inhabit.

    As Dr. Peter Fretwell from the British Antarctic Survey stated, "There is hope: we can cut our carbon emissions that are causing the warming. But if we don't, we will drive these iconic, beautiful birds to the verge of extinction." The window of opportunity to act is narrowing, emphasizing the urgency of global efforts to mitigate climate change and protect Antarctic ecosystems.
    """
    )

elif current_section == "Conservation":
    st.header("Conservation: The Path Forward")

    st.write(
        """
    As our penguin tale reaches its climax, we find ourselves at a critical juncture. The data we've explored paints a complex picture of Antarctic penguin populations in the face of climate change. Let's synthesize our findings and chart a course for the future.
    """
    )

    st.subheader("Synthesis of Findings")
    st.write(
        """
    1. Species-Specific Impacts: We've seen that different penguin species respond differently to climate change. While some species like the Gentoo penguins show adaptability, others like the Emperor penguins face severe threats due to their dependence on sea ice.

    2. Climate-Population Relationship: Our data reveals a complex relationship between temperature changes and penguin populations. While there's a general warming trend, its impact on penguins isn't uniform across species or locations.

    3. Site-Specific Variations: Some breeding sites have remained stable or even seen population increases, while others have experienced dramatic declines. This highlights the importance of local factors in addition to global climate trends.

    4. Urgency of Action: The catastrophic events we've observed, such as the loss of thousands of Emperor penguin chicks due to early ice breakup, underscore the immediate and severe threats posed by climate change.
    """
    )

    st.subheader("Generalizations and Implications")
    st.write(
        """
    1. Indicator Species: Penguins serve as crucial indicators of the overall health of the Antarctic ecosystem. Their struggles signal broader ecological challenges that extend beyond just these charismatic birds.

    2. Ecosystem Interconnectedness: Changes in penguin populations reflect alterations in the entire Antarctic food web, from krill to fish populations. This emphasizes the need for holistic ecosystem management.

    3. Global Climate Action: The fate of Antarctic penguins is inextricably linked to global climate trends. This implies that effective conservation requires not just local protection measures, but global efforts to mitigate climate change.

    4. Adaptive Management: Given the variability in how different species and colonies are affected, conservation strategies need to be adaptive and tailored to specific contexts.
    """
    )

    st.subheader("Key Takeaways for the Audience")
    st.write(
        """
    1. Urgency of Climate Action: The plight of Antarctic penguins is a vivid illustration of the real-time impacts of climate change. It's not a future problem – it's happening now.

    2. Importance of Data and Monitoring: Continued research and monitoring are crucial for understanding changes and informing conservation strategies. Support for scientific efforts is vital.

    3. Individual Impact: While the challenges are global, individual actions matter. Reducing your carbon footprint, supporting conservation organizations, and spreading awareness all contribute to the solution.

    4. Hope Through Action: Despite the dire situation for some penguin populations, our data also shows resilience and adaptability. With concerted conservation efforts and climate action, we can make a positive difference.
    """
    )

    st.subheader("Call to Action")
    st.write(
        """
    As we conclude our data journey through the world of Antarctic penguins, remember that you have the power to impact their future. Here's how you can help:
    """
    )

    col1, col2 = st.columns(2)
    with col1:
        st.write(
            """
        1. Reduce Your Carbon Footprint:
           - Calculate your carbon footprint and find ways to reduce it.
           - Support renewable energy initiatives.
           - Choose sustainable transportation options.

        2. Support Conservation Organizations:
           - Donate to or volunteer with organizations like Oceanites, WWF, or the Antarctic and Southern Ocean Coalition.
           - Participate in citizen science projects related to penguin conservation.
        """
        )
    with col2:
        st.write(
            """
        3. Educate and Advocate:
           - Share what you've learned about Antarctic penguins and climate change.
           - Advocate for policies that address climate change and protect Antarctic ecosystems.

        4. Make Informed Choices:
           - If visiting Antarctica, choose eco-friendly tour operators.
           - Support companies with strong environmental commitments.
        """
        )

    st.write(
        """
    Remember, the story of Antarctic penguins is still being written, and you can play a part in ensuring it has a positive ending. Every action, no matter how small, contributes to the larger effort of protecting these iconic birds and their fragile ecosystem.
    """
    )

    st.subheader("Explore Further and Stay Informed")
    st.write(
        """
    Continue your engagement with Antarctic penguin conservation by exploring these resources:
    """
    )

    # Keep your existing "Sources" section here
    st.subheader("Sources")
    st.write("- [Penguin Map Project](https://www.penguinmap.com/).")
    st.write(
        "- [Climate Change Data](https://climatedata.imf.org/pages/climatechange-data)."
    )
    st.write(
        "- [Penguins in Zoos](https://jpn-psa.jp/en/forefront-of-avian-conservation-6-for-the-future-of-the-humboldt-penguin-spheniscus-humboldti/#:~:text=Currently%2C%20over%204%2C000%20penguins%20from,in%20zoos%20and%20aquariums%20worldwide.)."
    )
    st.write(
        "- [Penguins in wildlife](https://www.bas.ac.uk/about/antarctica/wildlife/penguins/)."
    )
    st.write(
        "- [Penguins species sizes](https://www.kaggle.com/datasets/parulpandey/palmer-archipelago-antarctica-penguin-data?select=penguins_size.csv)."
    )
    st.write(
        "- [Climate change: Thousands of penguins die in Antarctic ice breakup](https://www.bbc.com/news/science-environment-66492767)."
    )
    st.write(
        "- [Emperor penguins lost thousands of chicks to melting ice last year](https://www.sciencenews.org/article/antarctica-emperor-penguins-endangered-climate)."
    )

    st.subheader("Leave a Comment")
    st.write(
        """
    We value your thoughts and feedback. Please share your reflections on the penguin data story, 
    any insights you've gained, or actions you plan to take for penguin conservation.
    """
    )

    # File to store comments
    COMMENTS_FILE = "penguin_comments.csv"

    # Function to load comments
    def load_comments():
        if os.path.exists(COMMENTS_FILE):
            return pd.read_csv(COMMENTS_FILE)
        return pd.DataFrame(columns=["Timestamp", "Name", "Comment"])

    # Function to save a comment
    def save_comment(name, comment):
        comments_df = load_comments()
        new_comment = pd.DataFrame(
            {
                "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "Name": [name if name else "Anonymous"],
                "Comment": [comment],
            }
        )
        comments_df = pd.concat([comments_df, new_comment], ignore_index=True)
        comments_df.to_csv(COMMENTS_FILE, index=False)

    # Input fields for new comment
    user_comment = st.text_area("Your comment:", height=150)
    user_name = st.text_input("Your name (optional):")

    if st.button("Submit Comment"):
        if user_comment:
            save_comment(user_name, user_comment)
            st.success(
                f"Thank you{' ' + user_name if user_name else ''} for your comment!"
            )
        else:
            st.warning("Please enter a comment before submitting.")

    # Display existing comments
    st.subheader("Recent Comments")
    comments_df = load_comments()
    if not comments_df.empty:
        for _, row in comments_df.iloc[::-1].iterrows():
            st.text(f"{row['Timestamp']} - {row['Name']}:")
            st.info(row["Comment"])
            st.markdown("---")
    else:
        st.write("No comments yet. Be the first to share your thoughts!")
