import pandas as pd


def check_column(df, file_col_name, col_name, by_camera='All'):
    """
    Count the number of images grouped by phone, camera, scene type, and col_name.

    :param df: Pandas data frame of EXIF data
    :param file_col_name: (str) Name of the column that contains the file names
    :param col_name: (str) Name of column to group images by in addition to phone, camera, scene type
    :param by_camera: (str) Either 'All', 'Front', 'Telephoto', 'Ultra', or 'Wide'
    :return: Pandas data frame
    """

    # create data frame
    phones = get_phones(df=df, file_col_name=file_col_name)
    cameras = get_cameras(df=df, file_col_name=file_col_name)
    scene_types = get_scene_type(df=df, file_col_name=file_col_name)
    col = get_column(df=df, col_name=col_name)
    df = pd.DataFrame({'phones': phones, 'cameras': cameras, 'scene_types': scene_types, 'var': col})

    # filter by camera
    if by_camera != 'All':
        df = df.query("cameras == @by_camera")

    # group and count
    df = df.groupby(['phones', 'cameras', 'scene_types', 'var']).size().reset_index()
    df = df.rename(columns={'var': col_name, 0: 'count'})
    return df


def check_missing_exif(df):
    return df.query('Aperture.isnull()', engine='python')


def count_images_by_camera(df, file_col_name):
    """
    Count the number of images grouped by phone, camera, and scene type.

    :param df: Pandas data frame of EXIF data
    :param file_col_name: (str) Name of the column that contains the file names
    :return: Pandas data frame
    """

    # create data frame
    phones = get_phones(df=df, file_col_name=file_col_name)
    cameras = get_cameras(df=df, file_col_name=file_col_name)
    scene_types = get_scene_type(df=df, file_col_name=file_col_name)
    df = pd.DataFrame({'phones': phones, 'cameras': cameras, 'scene_types': scene_types})

    # group and count
    df = df.groupby(['phones', 'cameras', 'scene_types']).size().reset_index()
    df = df.rename(columns={0: 'count'})
    return df


def get_cameras(df, file_col_name):
    """Get cameras as a list from the files names in the exif data frame, assuming that the folders use the
    naming convention '<model> <device> <camera>- <scene type>'"""
    folders = get_folders(df=df, file_col_name=file_col_name)
    strings = [s.split('-')[0].strip() for s in folders]
    return [s.split(' ')[2].strip() for s in strings]


def get_column(df, col_name):
    """Extract column from data frame as list"""
    return df[col_name].to_list()


def get_folders(df, file_col_name):
    """Extract folder names as a list from the files names in the exif data frame"""
    files = get_column(df=df, col_name=file_col_name)
    return [s.split('/')[-2] for s in files]


def get_models(df, file_col_name):
    """Get phone models as a list from the files names in the exif data frame, assuming that the folders use the
    naming convention '<model> <device> <camera>- <scene type>'"""
    folders = get_folders(df=df, file_col_name=file_col_name)
    strings = [s.split('-')[0].strip() for s in folders]
    return [s.split(' ')[0].strip() for s in strings]


def get_phones(df, file_col_name):
    """Get phone (model_device) as a list from the files names in the exif data frame, assuming that the folders use the
    naming convention '<model> <device> <camera>- <scene type>'"""
    folders = get_folders(df=df, file_col_name=file_col_name)
    strings = [s.split('-')[0].strip() for s in folders]
    return [s.split(' ')[0].strip() + '_' + s.split(' ')[1].strip() for s in strings]


def get_scene_type(df, file_col_name):
    """Extract scene type from folder names, assuming that the folders use the naming convention '<model> <device>
    <camera>-
    <scene type>'"""
    folders = get_folders(df=df, file_col_name=file_col_name)
    return [s.split('-')[-1].strip() for s in folders]


def read_exif(path, file_col_name):
    df = pd.read_csv(path)

    files = get_column(df=df, col_name=file_col_name)
    images = pd.Series([s.split('/')[-1].strip() for s in files])

    # drop file names that start with '.'
    df = df[~images.str.startswith('.')]

    return df
