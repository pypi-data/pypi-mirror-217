#ifndef DLPLAN_SRC_POLICY_READER_H_
#define DLPLAN_SRC_POLICY_READER_H_

#include <string>
#include <memory>


namespace dlplan {
namespace core {
    class SyntacticElementFactory;
}
namespace policy {
template<typename T>
class Feature;
template<typename T>
class FeatureFactory;
class BaseCondition;
class BaseEffect;
class Rule;
class Policy;
class PolicyBuilder;


class PolicyReaderImpl {
public:
    std::shared_ptr<const Policy> read(const std::string& data, PolicyBuilder& builder, core::SyntacticElementFactory& factory) const;
};

}
}

#endif
