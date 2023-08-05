// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/python/framework/op_reg_offset.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fpython_2fframework_2fop_5freg_5foffset_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fpython_2fframework_2fop_5freg_5foffset_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3021000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3021009 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/metadata_lite.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/unknown_field_set.h>
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_tensorflow_2fpython_2fframework_2fop_5freg_5foffset_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_tensorflow_2fpython_2fframework_2fop_5freg_5foffset_2eproto {
  static const uint32_t offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_tensorflow_2fpython_2fframework_2fop_5freg_5foffset_2eproto;
namespace tensorflow {
class OpRegOffset;
struct OpRegOffsetDefaultTypeInternal;
extern OpRegOffsetDefaultTypeInternal _OpRegOffset_default_instance_;
class OpRegOffsets;
struct OpRegOffsetsDefaultTypeInternal;
extern OpRegOffsetsDefaultTypeInternal _OpRegOffsets_default_instance_;
}  // namespace tensorflow
PROTOBUF_NAMESPACE_OPEN
template<> ::tensorflow::OpRegOffset* Arena::CreateMaybeMessage<::tensorflow::OpRegOffset>(Arena*);
template<> ::tensorflow::OpRegOffsets* Arena::CreateMaybeMessage<::tensorflow::OpRegOffsets>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace tensorflow {

// ===================================================================

class OpRegOffset final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.OpRegOffset) */ {
 public:
  inline OpRegOffset() : OpRegOffset(nullptr) {}
  ~OpRegOffset() override;
  explicit PROTOBUF_CONSTEXPR OpRegOffset(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  OpRegOffset(const OpRegOffset& from);
  OpRegOffset(OpRegOffset&& from) noexcept
    : OpRegOffset() {
    *this = ::std::move(from);
  }

  inline OpRegOffset& operator=(const OpRegOffset& from) {
    CopyFrom(from);
    return *this;
  }
  inline OpRegOffset& operator=(OpRegOffset&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const OpRegOffset& default_instance() {
    return *internal_default_instance();
  }
  static inline const OpRegOffset* internal_default_instance() {
    return reinterpret_cast<const OpRegOffset*>(
               &_OpRegOffset_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(OpRegOffset& a, OpRegOffset& b) {
    a.Swap(&b);
  }
  inline void Swap(OpRegOffset* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(OpRegOffset* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  OpRegOffset* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<OpRegOffset>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const OpRegOffset& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const OpRegOffset& from) {
    OpRegOffset::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(OpRegOffset* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.OpRegOffset";
  }
  protected:
  explicit OpRegOffset(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kNameFieldNumber = 1,
    kFilepathFieldNumber = 2,
    kStartFieldNumber = 3,
    kEndFieldNumber = 4,
  };
  // string name = 1;
  void clear_name();
  const std::string& name() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_name(ArgT0&& arg0, ArgT... args);
  std::string* mutable_name();
  PROTOBUF_NODISCARD std::string* release_name();
  void set_allocated_name(std::string* name);
  private:
  const std::string& _internal_name() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_name(const std::string& value);
  std::string* _internal_mutable_name();
  public:

  // string filepath = 2;
  void clear_filepath();
  const std::string& filepath() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_filepath(ArgT0&& arg0, ArgT... args);
  std::string* mutable_filepath();
  PROTOBUF_NODISCARD std::string* release_filepath();
  void set_allocated_filepath(std::string* filepath);
  private:
  const std::string& _internal_filepath() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_filepath(const std::string& value);
  std::string* _internal_mutable_filepath();
  public:

  // uint32 start = 3;
  void clear_start();
  uint32_t start() const;
  void set_start(uint32_t value);
  private:
  uint32_t _internal_start() const;
  void _internal_set_start(uint32_t value);
  public:

  // uint32 end = 4;
  void clear_end();
  uint32_t end() const;
  void set_end(uint32_t value);
  private:
  uint32_t _internal_end() const;
  void _internal_set_end(uint32_t value);
  public:

  // @@protoc_insertion_point(class_scope:tensorflow.OpRegOffset)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr name_;
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr filepath_;
    uint32_t start_;
    uint32_t end_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_tensorflow_2fpython_2fframework_2fop_5freg_5foffset_2eproto;
};
// -------------------------------------------------------------------

class OpRegOffsets final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.OpRegOffsets) */ {
 public:
  inline OpRegOffsets() : OpRegOffsets(nullptr) {}
  ~OpRegOffsets() override;
  explicit PROTOBUF_CONSTEXPR OpRegOffsets(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  OpRegOffsets(const OpRegOffsets& from);
  OpRegOffsets(OpRegOffsets&& from) noexcept
    : OpRegOffsets() {
    *this = ::std::move(from);
  }

  inline OpRegOffsets& operator=(const OpRegOffsets& from) {
    CopyFrom(from);
    return *this;
  }
  inline OpRegOffsets& operator=(OpRegOffsets&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const OpRegOffsets& default_instance() {
    return *internal_default_instance();
  }
  static inline const OpRegOffsets* internal_default_instance() {
    return reinterpret_cast<const OpRegOffsets*>(
               &_OpRegOffsets_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    1;

  friend void swap(OpRegOffsets& a, OpRegOffsets& b) {
    a.Swap(&b);
  }
  inline void Swap(OpRegOffsets* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(OpRegOffsets* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  OpRegOffsets* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<OpRegOffsets>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const OpRegOffsets& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const OpRegOffsets& from) {
    OpRegOffsets::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(OpRegOffsets* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.OpRegOffsets";
  }
  protected:
  explicit OpRegOffsets(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kOffsetsFieldNumber = 1,
  };
  // repeated .tensorflow.OpRegOffset offsets = 1;
  int offsets_size() const;
  private:
  int _internal_offsets_size() const;
  public:
  void clear_offsets();
  ::tensorflow::OpRegOffset* mutable_offsets(int index);
  ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::OpRegOffset >*
      mutable_offsets();
  private:
  const ::tensorflow::OpRegOffset& _internal_offsets(int index) const;
  ::tensorflow::OpRegOffset* _internal_add_offsets();
  public:
  const ::tensorflow::OpRegOffset& offsets(int index) const;
  ::tensorflow::OpRegOffset* add_offsets();
  const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::OpRegOffset >&
      offsets() const;

  // @@protoc_insertion_point(class_scope:tensorflow.OpRegOffsets)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::OpRegOffset > offsets_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_tensorflow_2fpython_2fframework_2fop_5freg_5foffset_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// OpRegOffset

// string name = 1;
inline void OpRegOffset::clear_name() {
  _impl_.name_.ClearToEmpty();
}
inline const std::string& OpRegOffset::name() const {
  // @@protoc_insertion_point(field_get:tensorflow.OpRegOffset.name)
  return _internal_name();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void OpRegOffset::set_name(ArgT0&& arg0, ArgT... args) {
 
 _impl_.name_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:tensorflow.OpRegOffset.name)
}
inline std::string* OpRegOffset::mutable_name() {
  std::string* _s = _internal_mutable_name();
  // @@protoc_insertion_point(field_mutable:tensorflow.OpRegOffset.name)
  return _s;
}
inline const std::string& OpRegOffset::_internal_name() const {
  return _impl_.name_.Get();
}
inline void OpRegOffset::_internal_set_name(const std::string& value) {
  
  _impl_.name_.Set(value, GetArenaForAllocation());
}
inline std::string* OpRegOffset::_internal_mutable_name() {
  
  return _impl_.name_.Mutable(GetArenaForAllocation());
}
inline std::string* OpRegOffset::release_name() {
  // @@protoc_insertion_point(field_release:tensorflow.OpRegOffset.name)
  return _impl_.name_.Release();
}
inline void OpRegOffset::set_allocated_name(std::string* name) {
  if (name != nullptr) {
    
  } else {
    
  }
  _impl_.name_.SetAllocated(name, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.name_.IsDefault()) {
    _impl_.name_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:tensorflow.OpRegOffset.name)
}

// string filepath = 2;
inline void OpRegOffset::clear_filepath() {
  _impl_.filepath_.ClearToEmpty();
}
inline const std::string& OpRegOffset::filepath() const {
  // @@protoc_insertion_point(field_get:tensorflow.OpRegOffset.filepath)
  return _internal_filepath();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void OpRegOffset::set_filepath(ArgT0&& arg0, ArgT... args) {
 
 _impl_.filepath_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:tensorflow.OpRegOffset.filepath)
}
inline std::string* OpRegOffset::mutable_filepath() {
  std::string* _s = _internal_mutable_filepath();
  // @@protoc_insertion_point(field_mutable:tensorflow.OpRegOffset.filepath)
  return _s;
}
inline const std::string& OpRegOffset::_internal_filepath() const {
  return _impl_.filepath_.Get();
}
inline void OpRegOffset::_internal_set_filepath(const std::string& value) {
  
  _impl_.filepath_.Set(value, GetArenaForAllocation());
}
inline std::string* OpRegOffset::_internal_mutable_filepath() {
  
  return _impl_.filepath_.Mutable(GetArenaForAllocation());
}
inline std::string* OpRegOffset::release_filepath() {
  // @@protoc_insertion_point(field_release:tensorflow.OpRegOffset.filepath)
  return _impl_.filepath_.Release();
}
inline void OpRegOffset::set_allocated_filepath(std::string* filepath) {
  if (filepath != nullptr) {
    
  } else {
    
  }
  _impl_.filepath_.SetAllocated(filepath, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.filepath_.IsDefault()) {
    _impl_.filepath_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:tensorflow.OpRegOffset.filepath)
}

// uint32 start = 3;
inline void OpRegOffset::clear_start() {
  _impl_.start_ = 0u;
}
inline uint32_t OpRegOffset::_internal_start() const {
  return _impl_.start_;
}
inline uint32_t OpRegOffset::start() const {
  // @@protoc_insertion_point(field_get:tensorflow.OpRegOffset.start)
  return _internal_start();
}
inline void OpRegOffset::_internal_set_start(uint32_t value) {
  
  _impl_.start_ = value;
}
inline void OpRegOffset::set_start(uint32_t value) {
  _internal_set_start(value);
  // @@protoc_insertion_point(field_set:tensorflow.OpRegOffset.start)
}

// uint32 end = 4;
inline void OpRegOffset::clear_end() {
  _impl_.end_ = 0u;
}
inline uint32_t OpRegOffset::_internal_end() const {
  return _impl_.end_;
}
inline uint32_t OpRegOffset::end() const {
  // @@protoc_insertion_point(field_get:tensorflow.OpRegOffset.end)
  return _internal_end();
}
inline void OpRegOffset::_internal_set_end(uint32_t value) {
  
  _impl_.end_ = value;
}
inline void OpRegOffset::set_end(uint32_t value) {
  _internal_set_end(value);
  // @@protoc_insertion_point(field_set:tensorflow.OpRegOffset.end)
}

// -------------------------------------------------------------------

// OpRegOffsets

// repeated .tensorflow.OpRegOffset offsets = 1;
inline int OpRegOffsets::_internal_offsets_size() const {
  return _impl_.offsets_.size();
}
inline int OpRegOffsets::offsets_size() const {
  return _internal_offsets_size();
}
inline void OpRegOffsets::clear_offsets() {
  _impl_.offsets_.Clear();
}
inline ::tensorflow::OpRegOffset* OpRegOffsets::mutable_offsets(int index) {
  // @@protoc_insertion_point(field_mutable:tensorflow.OpRegOffsets.offsets)
  return _impl_.offsets_.Mutable(index);
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::OpRegOffset >*
OpRegOffsets::mutable_offsets() {
  // @@protoc_insertion_point(field_mutable_list:tensorflow.OpRegOffsets.offsets)
  return &_impl_.offsets_;
}
inline const ::tensorflow::OpRegOffset& OpRegOffsets::_internal_offsets(int index) const {
  return _impl_.offsets_.Get(index);
}
inline const ::tensorflow::OpRegOffset& OpRegOffsets::offsets(int index) const {
  // @@protoc_insertion_point(field_get:tensorflow.OpRegOffsets.offsets)
  return _internal_offsets(index);
}
inline ::tensorflow::OpRegOffset* OpRegOffsets::_internal_add_offsets() {
  return _impl_.offsets_.Add();
}
inline ::tensorflow::OpRegOffset* OpRegOffsets::add_offsets() {
  ::tensorflow::OpRegOffset* _add = _internal_add_offsets();
  // @@protoc_insertion_point(field_add:tensorflow.OpRegOffsets.offsets)
  return _add;
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::OpRegOffset >&
OpRegOffsets::offsets() const {
  // @@protoc_insertion_point(field_list:tensorflow.OpRegOffsets.offsets)
  return _impl_.offsets_;
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__
// -------------------------------------------------------------------


// @@protoc_insertion_point(namespace_scope)

}  // namespace tensorflow

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fpython_2fframework_2fop_5freg_5foffset_2eproto
