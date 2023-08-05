# commands.py

from typing import List
from dataclasses import dataclass

from represent import BaseModel

__all__ = [
    "CommandsGenerator"
]

@dataclass(repr=False, slots=True)
class CommandsGenerator(BaseModel):
    """A class to represent the execution commands factory."""

    MESH_NAME = "mesh.obj"

    GROUP_SIZE = 3

    path: str
    source: str
    output: str
    images_count: int
    group_size: int = GROUP_SIZE
    name: str = MESH_NAME

    def camera_initialization(self) -> str:
        """
        Runs the process in the command line.

        :return: The command string.
        """

        bin_path = self.path + "\\aliceVision_cameraInit.exe"
        destination_dir = self.output + f"/{self.camera_initialization.__name__}/"

        command = bin_path + " "
        command += (
            f"--defaultFieldOfView {45.0} --verboseLevel info "
            f"--sensorDatabase \"\" --allowSingleView {1} "
            f"--imageFolder \"{self.source}\" "
            f"--output \"{destination_dir}cameraInit.sfm\""
        )

        return command
    # end camera_initialization

    def features_extraction(self) -> str:
        """
        Runs the process in the command line.

        :return: The command string.
        """

        src_sfm = self.output + f"/{self.camera_initialization.__name__}/cameraInit.sfm"
        bin_path = self.path + "\\aliceVision_featureExtraction.exe"
        destination_dir = self.output + f"/{self.features_extraction.__name__}/"

        command = bin_path + " "
        command += (
            f"--describerTypes sift --forceCpuExtraction {True} "
            f"--verboseLevel info --describerPreset normal "
            f"--rangeStart {0} --rangeSize {self.images_count} "
            f"--input \"{src_sfm}\" "
            f"--output \"{destination_dir}\" "
        )

        return command
    # end features_extraction

    def images_matching(self) -> str:
        """
        Runs the process in the command line.

        :return: The command string.
        """

        src_sfm = self.output + f"/{self.camera_initialization.__name__}/cameraInit.sfm"
        src_features = self.output + f"/{self.features_extraction.__name__}/"
        dst_matches = self.output + f"/{self.images_matching.__name__}/imageMatches.txt"
        bin_path = self.path + "\\aliceVision_imageMatching.exe"

        command = bin_path + " "
        command += (
            f"--minNbImages {200} --tree --maxDescriptors {500} "
            f"--verboseLevel info --weights --nbMatches {50} "
            f"--input \"{src_sfm}\" --featuresFolder \"{src_features}\" "
            f"--output \"{dst_matches}\""
        )

        return command
    # end images_matching

    def features_matching(self) -> str:
        """
        Runs the process in the command line.

        :return: The command string.
        """

        src_sfm = self.output + f"/{self.camera_initialization.__name__}/cameraInit.sfm"
        src_features = self.output + f"/{self.features_extraction.__name__}/"
        src_image_matches = self.output + f"/{self.images_matching.__name__}/imageMatches.txt"
        dst_matches = self.output + f"/{self.features_matching.__name__}"
        bin_path = self.path + "\\aliceVision_featureMatching.exe"

        command = bin_path + " "
        command += (
            f"--verboseLevel info --describerTypes sift "
            f"--maxMatches {0} --exportDebugFiles {False} "
            f"--savePutativeMatches {False} --guidedMatching {False} "
            f"--geometricEstimator acransac --geometricFilterType fundamental_matrix "
            f"--maxIteration {2048} --distanceRatio {0.8} "
            f"--photometricMatchingMethod ANN_L2 "
            f"--imagePairsList \"{src_image_matches}\" "
            f"--input \"{src_sfm}\" "
            f"--featuresFolders \"{src_features}\" "
            f"--output \"{dst_matches}\""
        )

        return command
    # end features_matching

    def structure_from_motion_building(self) -> str:
        """
        Runs the process in the command line.

        :return: The command string.
        """

        src_sfm = self.output + f"/{self.camera_initialization.__name__}/cameraInit.sfm"
        src_features = self.output + f"/{self.features_extraction.__name__}/"
        src_matches = self.output + f"/{self.features_matching.__name__}"
        dst_dir = self.output + f"/{self.structure_from_motion_building.__name__}"
        bin_path = self.path + "\\aliceVision_incrementalSfm.exe"

        command = bin_path + " "
        command += (
            f"--minAngleForLandmark {2.0} "
            f"--minNumberOfObservationsForTriangulation {2} "
            f"--maxAngleInitialPair {40.0} --maxNumberOfMatches {0} "
            f"--localizerEstimator acransac --describerTypes sift "
            f"--lockScenePreviouslyReconstructed {False} "
            f"--localBAGraphDistance {1} "
            f"--initialPairA "" --initialPairB "" "
            f"--interFileExtension .ply --useLocalBA {True} "
            f"--minInputTrackLength {2} --useOnlyMatchesFromInputFolder {False} "
            f"--verboseLevel info --minAngleForTriangulation {3.0} "
            f"--maxReprojectionError {4.0} --minAngleInitialPair {5.0} "
            f"--input \"{src_sfm}\" "
            f"--featuresFolders \"{src_features}\" "
            f"--matchesFolders \"{src_matches}\" "
            f"--outputViewsAndPoses \"{dst_dir}/cameras.sfm\" "
            f"--extraInfoFolder \"{dst_dir}\" "
            f"--output \"{dst_dir}/bundle.sfm\""
        )

        return command
    # end structure_from_motion_building

    def dense_scene_preparation(self) -> str:
        """
        Runs the process in the command line.

        :return: The command string.
        """

        src_sfm = self.output + f"/{self.structure_from_motion_building.__name__}/bundle.sfm"
        dst_dir = self.output + f"/{self.dense_scene_preparation.__name__}"
        bin_path = self.path + "\\aliceVision_prepareDenseScene.exe"

        command = bin_path + " "
        command += f"--verboseLevel info --input \"{src_sfm}\" "
        command += f"--output \"{dst_dir}\""

        return command
    # end dense_scene_preparation

    def camera_connection(self) -> str:
        """
        Runs the process in the command line.

        :return: The command string.
        """

        src_ini = self.output + f"/{self.dense_scene_preparation.__name__}/mvs.ini"
        bin_path = self.path + "\\aliceVision_cameraConnection.exe"

        command = bin_path
        command += f" --verboseLevel info --ini \"{src_ini}\""

        return command
    # end camera_connection

    def depth_mapping(self) -> str:
        """
        Runs the process in the command line.

        :return: The command string.
        """

        src_ini = self.output + f"/{self.dense_scene_preparation.__name__}/mvs.ini"
        bin_path = self.path + "\\aliceVision_depthMapEstimation.exe"
        dst_dir = self.output + f"/{self.depth_mapping.__name__}"

        command = bin_path + " "
        command += (
            f"--sgmGammaC {5.5} --sgmWSH {4} --refineGammaP {8.0} "
            f"--refineSigma {15} --refineNSamplesHalf {150} "
            f"--sgmMaxTCams {10} --refineWSH {3} --downscale {2} "
            f"--refineMaxTCams {6} --verboseLevel info --refineGammaC {15.5} "
            f"--sgmGammaP {8.0} --refineNiters {100} --refineNDepthsToRefine {31} "
            f"--refineUseTcOrRcPixSize {False} "
            f"--ini \"{src_ini}\" "
            f"--output \"{dst_dir}\" "
        )

        return command
        # end for
    # end depth_mapping

    def depth_mapping_groups(self) -> List[str]:
        """
        Runs the process in the command line.

        :return: The command string.
        """

        command = self.depth_mapping()

        groups = int(
            (self.images_count + (self.group_size - 1)) /
            self.group_size
        )

        commands = []

        for i, group_iter in enumerate(range(groups)):
            group_start = self.group_size * group_iter
            group_size = min(
                self.group_size, self.images_count - group_start
            )

            group_command = command + (
                f"--rangeStart {int(group_start)} "
                f"--rangeSize {int(group_size)}"
            )

            commands.append(group_command)
        # end for

        return commands
    # end depth_mapping_groups

    def depth_map_filtering(self) -> str:
        """
        Runs the process in the command line.

        :return: The command string.
        """

        bin_path = self.path + "\\aliceVision_depthMapFiltering.exe"
        dst_dir = self.output + f"/{self.depth_map_filtering.__name__}"
        src_ini = self.output + f"/{self.dense_scene_preparation.__name__}/mvs.ini"
        src_depth_dir = self.output + f"/{self.depth_mapping.__name__}"

        command = bin_path + " "
        command += (
            f"--minNumOfConsistensCamsWithLowSimilarity {4} "
            f"--minNumOfConsistensCams {3} --verboseLevel info --pixSizeBall {0} "
            f"--pixSizeBallWithLowSimilarity {0} --nNearestCams {10} "
            f"--ini \"{src_ini}\" "
            f"--output \"{dst_dir}\" "
            f"--depthMapFolder \"{src_depth_dir}\""
        )

        return command
    # end depth_map_filtering

    def meshing(self) -> str:
        """
        Runs the process in the command line.

        :return: The command string.
        """

        bin_path = self.path + "\\aliceVision_meshing.exe"
        src_ini = self.output + f"/{self.dense_scene_preparation.__name__}/mvs.ini"
        src_depth_filter_dir = self.output + f"/{self.depth_map_filtering.__name__}"
        src_depth_map_dir = self.output + f"/{self.depth_mapping.__name__}"
        dst_dir = self.output + f"/{self.meshing.__name__}"

        command = bin_path + " "
        command += (
            f"--simGaussianSizeInit {10.0} --maxInputPoints {50000000}"
            " --repartition multiResolution "
            f"--simGaussianSize {10.0} --simFactor {15.0} --voteMarginFactor {4.0} "
            f"--contributeMarginFactor {2.0} --minStep {2} --pixSizeMarginFinalCoef {4.0} "
            f"--maxPoints {5000000} --maxPointsPerVoxel {1000000} "
            f"--angleFactor {15.0} --partitioning singleBlock "
            f"--minAngleThreshold {1.0} --pixSizeMarginInitCoef {2.0} "
            f"--refineFuse {True} --verboseLevel info "
            f"--ini \"{src_ini}\" "
            f"--depthMapFilterFolder \"{src_depth_filter_dir}\" "
            f"--depthMapFolder \"{src_depth_map_dir}\" "
            f"--output \"{dst_dir}/{self.name}\""
        )

        return command
    # end meshing

    def mesh_filtering(self) -> str:
        """
        Runs the process in the command line.

        :return: The command string.
        """

        bin_path = self.path + "\\aliceVision_meshFiltering.exe"
        src_mesh = self.output + f"/{self.meshing.__name__}/{self.name}"
        dst_mesh = self.output + f"/{self.mesh_filtering.__name__}/{self.name}"

        command = bin_path + " "
        command += (
            f"--verboseLevel info --removeLargeTrianglesFactor {60.0} "
            f"--iterations 5 --keepLargestMeshOnly {True} --lambda {1.0} "
            f"--input \"{src_mesh}\" "
            f"--output \"{dst_mesh}\""
        )

        return command
    # end mesh_filtering

    def texturing(self) -> str:
        """
        Runs the process in the command line.

        :return: The command string.
        """

        bin_path = self.path + "\\aliceVision_texturing.exe"
        src_mesh = self.output + f"/{self.mesh_filtering.__name__}/{self.name}"
        src_recon = self.output + f"/{self.meshing.__name__}/denseReconstruction.bin"
        src_ini = self.output + f"/{self.dense_scene_preparation.__name__}/mvs.ini"
        dst_dir = self.output + f"/{self.texturing.__name__}"

        command = bin_path + " "
        command += (
            f"--textureSide {8192} "
            f"--downscale {2} --verboseLevel info --padding {15} "
            f"--unwrapMethod Basic --outputTextureFileType png "
            f"--flipNormals {False} --fillHoles {False} "
            f"--inputDenseReconstruction \"{src_recon}\" "
            f"--inputMesh \"{src_mesh}\" "
            f"--ini \"{src_ini}\" "
            f"--output \"{dst_dir}\""
        )

        return command
    # end texturing
# end Executor