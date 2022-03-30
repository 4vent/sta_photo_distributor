import ui
import photos
from console import hud_alert
from dialogs import list_dialog

def compairString(large, small):
    for l, s in zip(large, small):
        if l == s:
            continue
        else:
            if ord(l) > ord(s):
                return True
            else:
                return False

def sortedAlbums(albumAssetCollections):
    sorted = []
    for AAC in albumAssetCollections:
        for i, s in enumerate(sorted):
            if not compairString(AAC.title, s.title):
                sorted.insert(i, AAC)
                break
        else:
            sorted.append(AAC)
    return sorted

num = 0
assets = photos.get_assets()
albums = photos.get_albums()

albums = sortedAlbums(albums)

def setNumWithChosePhoto(sender=None, selectedId=None):
    global num
    global albums
    global assets
    if selectedId == None:
        selectedId = photos.pick_asset(assets).local_id
    try:
        photos.get_asset_with_local_id(selectedId)
        selectedNum = [a.local_id for a in assets].index(selectedId)
        num = selectedNum
        update_img()
        return True
    except ValueError:
        return False
    
def get7img(center):
    global assets
    global v
    imgs = []
    for i in range(-3, 4):
        if 0 <= i + center < len(assets):
            if i == 0:
                imgs.append(assets[center + i].get_ui_image((v['Image4'].width*2, v['Image4'].height*2)))
            else:
                imgs.append(assets[center + i].get_ui_image((150, 150), True))
        else:
            imgs.append(None)
    return imgs

def update_img():
    global v
    global assets
    imageViews = [
        'Image1', 
        'Image2',
        'Image3',
        'Image4',
        'Image5',
        'Image6',
        'Image7'
        ]
    v['ImageTitle'].text = assets[num].local_id
    imgs = get7img(num)
    for i in range(7):
        if not i == 3:
            v[imageViews[i]].content_mode = ui.CONTENT_SCALE_ASPECT_FILL
            v[imageViews[i]].image = imgs[i]
        else:
            v[imageViews[i]][imageViews[i]].content_mode = ui.CONTENT_SCALE_ASPECT_FIT
            v[imageViews[i]][imageViews[i]].image = imgs[i]
    with open('last_editing.txt', 'w') as f:
        f.write(assets[num].local_id)

def next_img(sender=None):
    global num
    if num == len(assets) - 1:
        hud_alert('Latest Image')
        return
    else:
        num += 1
        update_img()

def prev_img(sender=None):
    global num
    if num == 0:
        return
    else:
        num -= 1
        update_img()

def selectAlbumWithDialog(sender):
    global albums
    global assets
    albumTitle = list_dialog(items=[a.title for a in albums])
    if not albumTitle == None:
        selectNum = [a.title for a in albums].index(albumTitle)
        albums[selectNum].add_assets([assets[num]])
    next_img()
    
def selectAlbumWithTable(sender):
    global albums
    global assets
    selectNum = sender.selected_row
    albums[selectNum].add_assets([assets[num]])
    v['AlbumTable'].selected_rows = []
    v['AlbumTable'].reload_data()
    hud_alert('add to ' + albums[selectNum].title, 'success', 0.5)
    next_img()
    
def tableview_cell_for_row(self, tableview, row):
    global albums
    # Create and return a cell for the given section/row
        
    # to get different cell types, pass subtitle or value1, or value2
    # to ui.TableViewCell() pass in as a string
    cell = ui.TableViewCell()
        
    cell.content_view.bg_color = None
    cell.content_view.alpha = 1
    cell.bg_color = (0.0, 0.0, 0.0, 0.5)
    cell.text_label.text_color = (1.0, 1.0, 1.0, 1.0)
    cell.text_label.text = albums[row].title
    cell.highlight_color = (0.1, 0.1, 0.1, 0.5)

    return cell

v = ui.load_view()

albumDataSource = ui.ListDataSource(items=[a.title for a in albums])

albumDataSource.tableview_cell_for_row = tableview_cell_for_row
v['AlbumTable'].data_source = albumDataSource
v['AlbumTable'].separator_color = (0.8, 0.8, 0.8, 1.0)

with open('last_editing.txt', 'r') as f:
    selectedId = f.readline()
isSuccess = setNumWithChosePhoto(selectedId=selectedId)
if not isSuccess:
    setNumWithChosePhoto()
update_img()

v.present('fullscreen')

v['Image4'].directional_lock_enabled = False
v['Image4'].content_size = (v['Image4'].width+1, v['Image4'].height+1)
